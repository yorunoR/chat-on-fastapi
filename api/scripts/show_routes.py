from fastapi.routing import APIRoute, APIWebSocketRoute, iter_route_contexts

from interfaces.main import api


def main() -> None:
    for route_context in iter_route_contexts(api.routes):
        route = route_context.original_route
        if isinstance(route, APIRoute):
            method = ",".join(sorted(route_context.methods))
            path = route_context.path
        elif isinstance(route, APIWebSocketRoute):
            method = "WS"
            # WebSocket は include 後のパスが route_context.path ではなく starlette_route に入る
            path = route_context.starlette_route.path
        else:
            continue
        handler_file = route.endpoint.__module__.replace(".", "/") + ".py"
        print(f"{method:<7} {path:<40} {handler_file}")


if __name__ == "__main__":
    main()
