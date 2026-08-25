from codex_domination.discovery import ThreadDiscoveryService, normalize_thread_list_response


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def model_dump(self, *, by_alias, mode):
        assert by_alias is True
        assert mode == "json"
        return self.payload


class FakeCodex:
    def __init__(self, response):
        self.response = response
        self.limit = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return None

    def thread_list(self, *, limit=None):
        self.limit = limit
        return self.response


def test_normalize_thread_list_response():
    response = FakeResponse(
        {
            "data": [
                {
                    "id": "thread-1",
                    "name": "Backend",
                    "cwd": "D:/FlowTracer-wt/backend",
                    "preview": "Implement BE-4",
                    "updatedAt": 123,
                }
            ]
        }
    )

    threads = normalize_thread_list_response(response)

    assert len(threads) == 1
    assert threads[0].thread_id == "thread-1"
    assert threads[0].name == "Backend"
    assert threads[0].cwd == "D:/FlowTracer-wt/backend"
    assert threads[0].updated_at == 123


def test_empty_thread_list_is_valid():
    assert normalize_thread_list_response(FakeResponse({"data": []})) == []


def test_missing_thread_id_is_rejected():
    try:
        normalize_thread_list_response(FakeResponse({"data": [{"name": "bad"}]}))
    except ValueError as exc:
        assert "valid id" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_service_uses_official_thread_list_surface():
    fake = FakeCodex(FakeResponse({"data": [{"id": "thread-2"}]}))
    service = ThreadDiscoveryService(codex_factory=lambda: fake)

    result = service.list_threads(limit=25)

    assert fake.limit == 25
    assert [thread.thread_id for thread in result] == ["thread-2"]
