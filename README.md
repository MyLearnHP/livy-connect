# Livy Connect
Based on _*`Python-requests`*_ library.

## Usage

```python
from livy_connect.livy_connect import LivyConnect


livy_connect = LivyConnect(
                    host='0.0.0.0' # Livy Host IP address
                    )
livy_connect.sessions_list() # List all Sessions
_id = livy_connect.create_session() # Create a new session
_status = livy_connect.session_status() # Get status of a created session
print(_status)
_status = livy_connect.session_status(session_id=1234) # Get status of a session by passing session id
print(_status)
```