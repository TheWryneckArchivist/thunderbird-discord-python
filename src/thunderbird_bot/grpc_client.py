from dataclasses import dataclass

import grpc


@dataclass(slots=True)
class ThunderbirdGrpcClient:
    endpoint: str

    def __post_init__(self) -> None:
        self.channel = grpc.aio.insecure_channel(self.endpoint)

    async def create_session(self, host_user_id: str, title: str, ruleset_version: str) -> dict:
        # Placeholder for generated gRPC stub call (SessionService.CreateSession)
        return {
            "session_id": "session-placeholder",
            "title": title,
            "ruleset_version": ruleset_version,
            "host_user_id": host_user_id,
        }

    async def join_session(self, session_id: str, user_id: str) -> dict:
        # Placeholder for generated gRPC stub call (SessionService.JoinSession)
        return {
            "session_id": session_id,
            "user_id": user_id,
            "status": "joined",
        }
