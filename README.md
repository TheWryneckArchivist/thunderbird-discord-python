# thunderbird-discord-python

Python services for:
- Discord companion bot (partial gameplay commands)
- Async workers for moderation/notifications/content tasks

## Commands

```bash
pip install -e .[dev]
python -m thunderbird_bot.main
python -m thunderbird_workers.worker
pytest
```

## Integrations

- gRPC endpoint: `GRPC_ENDPOINT`
- RabbitMQ: `RABBITMQ_URL`

## Private Python Feed

To install private packages, set `PYPI_EXTRA_INDEX_URL` or copy `pip.conf.example` to your local pip config.
