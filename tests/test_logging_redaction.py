from __future__ import annotations

import logging
import os

from app.logging_config import RedactingFilter


def test_redaction_filter_redacts_secrets():
    """RedactingFilter should replace secret values with [REDACTED]."""
    # Set a test secret
    test_secret = "my_secret_token_12345"
    os.environ["HF_TOKEN"] = test_secret
    
    # Create a log record with the secret
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg=f"Connecting with token {test_secret}",
        args=(),
        exc_info=None,
    )
    
    # Apply filter
    filter_obj = RedactingFilter()
    result = filter_obj.filter(record)
    
    # Should return True and redact the secret
    assert result is True
    assert test_secret not in record.msg
    assert "[REDACTED]" in record.msg
    
    # Cleanup
    del os.environ["HF_TOKEN"]


def test_redaction_all_keys():
    """All keys in REDACT_KEYS should be redacted."""
    test_secrets = {
        "HF_TOKEN": "hf_test_123",
        "GITHUB_TOKEN": "gh_test_456",
        "POSTGRES_PASSWORD": "pg_pass_789",
        "DO_PG_PASSWORD": "do_pass_abc",
    }
    
    for key, value in test_secrets.items():
        os.environ[key] = value
        
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg=f"Using {key}: {value}",
            args=(),
            exc_info=None,
        )
        
        filter_obj = RedactingFilter()
        filter_obj.filter(record)
        
        assert value not in record.msg, f"{key} was not redacted"
        assert "[REDACTED]" in record.msg
        
        del os.environ[key]


def test_redaction_partial_match():
    """Redaction should work when secret appears in longer string."""
    os.environ["HF_TOKEN"] = "abc123"
    
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Token abc123xyz should be redacted",
        args=(),
        exc_info=None,
    )
    
    filter_obj = RedactingFilter()
    filter_obj.filter(record)
    
    # The exact secret value should be redacted
    assert "abc123" not in record.msg
    assert "[REDACTED]" in record.msg
    
    del os.environ["HF_TOKEN"]


def test_redaction_no_false_positives():
    """Should not redact when secret is not in message."""
    os.environ["HF_TOKEN"] = "secret_token"
    
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="This message has no secrets",
        args=(),
        exc_info=None,
    )
    
    original_msg = record.msg
    filter_obj = RedactingFilter()
    filter_obj.filter(record)
    
    # Message should be unchanged
    assert record.msg == original_msg
    
    del os.environ["HF_TOKEN"]

