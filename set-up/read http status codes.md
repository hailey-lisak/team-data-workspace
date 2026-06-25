read http status codes
docker run --rm -p 8000:8000 team-data-workspace:latest
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "name": "Alice"
  }'
curl -X POST http://localhost:8000/workspaces \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Engineering",
    "user_id": "usr_12345678"
  }'
curl -X POST http://localhost:8000/workspaces/ws_12345678/records/import \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bob",
    "email": "bob@example.com",
    "company": "Acme Corp",
    "city": "San Francisco",
    "notes": "Contact next week"
  }'



when you make changes, you have to make a new image every time, push image onto docker, run (understand docker file and code requests)

create subfolder databases for all the scripts

don't forget to take remove the hardcoding done in part 1

docker build takes docker composed file and pushes file to local folder where the location is
docker run takes file and pushes to docker engine thats running locally

**HTTPS STATUS CODES****
download set up pstgres
create specific folder whcih should say database and inside create scripts
  first script, all necessary tables then write a TEST script (dont integrate with actual code) to connect to database from a python file
then use copilot for orms (3 orms users, records, workspaces)




create a database, use copilot to generate models based off of database

make sure not to hardcode name

create a file where you can save credentials (.env file) and .gitignore and add .env to .gitignore


HTTP STATUS CODES:
100-199: informational responses
  100: continue (client should continue the request or ignore the response if the request is already finished)
  101: switching protocols (sent in response to an upgrade request header from the client and indicates the protocol the server is switching to)
  102: processing (used in webDAV contexts to indicate that a request has been recieved by the server, but no status was available at the time of the response)
  103: early hints (intended to be used with the Link header, letting the user agent start preloading resources while the server prepares a response or preconnect to an origin from which the page will need resources)
200-299: successful responses
  200: OK (the request succeeded, the meaning of "success" depends on the HTTP method---GET, HEAD, PUT/POST, TRACE)
  201: created (the request succeeded, and a new resource was created as a result; typically the response sent after POST and some PUT requests)
  202: accepted (request has been recieved but not yet acted upon; noncomittal->intended for cases where another process or serv er handles the request, or for batch processing)
  203: non-authoritative information (means the returned metadata is not exactly the same as is available from the origin server, but is collected from a local or a third-party copy; mostly used for mirrors or backups of another resource)
  204: no content (there is no content to send for this request, but the headers are useful; the user agent may update its cached headers for this resource with the new ones)
  205: reset content (tells user agent to reset the document which sent this request)
  206: partial content (used in response to a range request when the client has requested a part or parts of a resource)
  207 (WebDAV): multi-status (conveys info about multiple resources, for situations where multiple status codes might be appropriate)
  208 (WebDAV): already reported (used inside a <dav:propstat> response ekement to avoid repeatedly enumerating the internal members of multiple bindings to the same collection)
  226 (HTTP Delta encoding): IM used (server has fulfilled a GET request for the resource, and the response is a representation of the result of one or more instance-manipulations applied to the current instance)
300-399: redirectional responses
  300: multiple choices (in agent-driven content negotiation, the request has more than one possible repsonse and the user agent or user should choose one of them. there is no standardized way for clients to automatically choose one of the responses, so this is rarely used)
  301: moved permanently (the URL of the requested resource has been changed permanently; the new URL is given in respoonse)
  302: found (the URI of the requested resources has been changed temporarily; further changes int eh URI might be made in the future, so the same URI should be used by the client in future requests)
  303: see other (server is sent this response to direct the client to get the requested resource at another URI with a GET request)
  304: not modified (used for caching purposes; tells the client that the response has not been modified, so the client can continue to use the same cached version of the response)
  307: temporary redirect (directs the client to get the requested resource at another URI with the same mehtod that was used in the prior request; same semantics as the 302 Found response code, with the exception that the user agent must not change the HTTP method used)
  308: permanent redirect (resource is now permanently located at another URI specified by the Locatio response header; once again, user agent must not change HTTP mehtod used)
400-499: client error responses 
  400: bad request (server cannot or will not process the request due to something that is percieved to be a client error)
  401: unauthorized (means "unauthenticated"; client must authenticate itself to get the requested response)
  402: payment required
  403: foridden (client doesn't have access rights to the content)
  404: not found (server cannot find the requested resource)
  405: method not allowed (request method is known by the server but is not supported by the targer resource)
  406: not acceptable (sent when web server, after performing sever-driven content negotiation, doesn't find any content that conforms to the criteria given by the user agent)
  407: proxy authentication required (authentication is needed to by done by a proxy)
  408: request timeout (sent on an idle connection by some servers, even without any previous request by the client; means that the server would like to shut down this unused connected; some servers may shut down without sending this message)
  409: conflict (response sent when a request conflicts with the current state of the server)
  410: gone (sent when the requested content has been permanently deleted from serever, with no forwarding address; clients are expected to remove thier caches and links to the resource; APIs should not feel compelled to indicate resources that have been deleted with this status code)
  411: length required (server rejected the reuqest because the content-length headere field is not defined and the server requires it)
  412: precondition failed (in conditional requests, the client has indicated preconditions in its headers which the server does not meet)
  413: content too large (request body is larger than limits defined by server)
  414: URI too long (the URI requested by the client is longer than the server is willing to interpret)
  415: unsupported media type (the media format of the requested data is not supported by the server, so the server is rejecting the request)
  416: range not satisfiable
  417: expectation failed
  418: I'm a teapot (server refuses to attempt to bew coffee with a teapot)
  421: misdirected request
  422 (WebDAV): unprocessable content
  423 (WebDAV): locked
  424 (WebDAV): failed dependency (request failed due to a failure of a previous request)
  425: too early (server is unwilling to risk processing a request that might be replayed)
  426: upgrade required
  428: precondition required
  429: too many requests
  431: request header fields too large
  451: unavailable for legal reasons
500-599: server error responses
  500: internal server error (server has encountered a situation it does not know how to handle; error is generic)
  501: not implemented (request mehtod is not supported by the server and cannot be handled; GET and HEAD are the only methods that servers are required to support)
  502: bad gateway (the server, while working as a gateway to get a response needed to handle the request, got an invalid response)
  503: service unavailable (server is not ready to handle the request)
  504: gateway timeout 
  505: HTTP version not supported 
  506: variant also negotiates (server has an internal configuration error: during content negotation, the chosen variant is configured to engage in content negotation itself, which results in circular references when creating responses)
  507 (WebDAV): insuffiecient storage (server is unable to store the representation needed to successfully complete the request)
  508 (WebDAV): loop detected (infinite loop detected)
  510: not extended (the client request declares an HTTP extension that should be used to pocess the request, but the extension is not supported)
  511: nettwork authentication required



