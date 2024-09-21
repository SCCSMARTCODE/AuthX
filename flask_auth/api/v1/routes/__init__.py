"""
This is the file that manages the Endpoint Resource

"""


def get_namespace_update():
    from . basic_user_auth import basic_user_ns

    namespace_update = [
                (basic_user_ns, '/api/vi'),
            ]
    return namespace_update
