# Key Decisions

## Backend
- `@action(detail=True)` → single endpoint for notes list/create
- Explicit test paths → fixes Django discovery bug (16/16 tests)
- needed to change the docker-compose a little otherwise I needed to update some things on my PC for local development. I reverted it for the CI.
- added a devcontainer. This because I dont install all tools native on my pc.

## Frontend  
- Angular 17 standalone components + RxJS polling (5s interval)
- Build-only CI

## CI Pipeline
- `docker compose run --rm` → isolated tests
- Backend 16 tests + frontend build → green ✅
- I had no experience in CI-CD with github yet. I am used to azure devops with on prem agents. (was a little different but maybe even a little better for what ive seen now.)

## Time: spend
Backend: 40min | Frontend: 1-2h | Tests/CI: 1h

## Trade offs:
- UI i didnt spend any time on creating a sleek design.
- Unit test for UI (done this before wanted to look more in the Python ones which I didnt do before)

## Next
1. Ui styling
2. Meeting model ordering
3. Frontend unit tests  
4. WebSockets
