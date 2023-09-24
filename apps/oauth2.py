from django.contrib.auth.hashers import make_password
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from apps.models import User
from apps.token import get_tokens_for_user


# eyJhbGciOiJSUzI1NiIsImtpZCI6IjZmNzI1NDEwMWY1NmU0MWNmMzVjOTkyNmRlODRhMmQ1NTJiNGM2ZjEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI5MTg2ODUzNTExMTItMTQ4MTBrdXExbGlsZjNtc2hkaWM2Y2lvcmMzbHE2dmguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI5MTg2ODUzNTExMTItMTQ4MTBrdXExbGlsZjNtc2hkaWM2Y2lvcmMzbHE2dmguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDg4NjM4NjY5NTU0MTIwMjg0NjUiLCJlbWFpbCI6InhvbGlxdWxvdjExNkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmJmIjoxNjk1MjExODczLCJuYW1lIjoiTydyb2xiZWsgWG9saXF1bG92IiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xKUmk5LVZwVXFiblRQTjhfbzJtWkczZkJGejhIRHRhWnpHeGlRREhzPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6Ik8ncm9sYmVrIiwiZmFtaWx5X25hbWUiOiJYb2xpcXVsb3YiLCJsb2NhbGUiOiJydSIsImlhdCI6MTY5NTIxMjE3MywiZXhwIjoxNjk1MjE1NzczLCJqdGkiOiI5MmQ5ZmUyYmJiYmY2NTI2YmY3NDQ2YTRlMTUxZmJjMTQ5ZjEyZjY2In0.mhoX-lLAuHHgzUW8tSxA9cXZOixDRlHXX2ONVxWtr5IKzxoR7JEeTaJ0kY8NYNceKKFjm-kadDqQLeLxyarPzO2pBuS1y_vt16KBa1tgHif3_mA8r7785ZMsIN5qLDCRs9rNU3MRwkBBhTtiLWXPpdxQ3lLT8fWj2f_4fMD7w9l9sGKjdVfUSnNHKuFCOgCfVGhqLSEwrDpW8ITVi2cxbBTAF_5TxdjzG7pEV9_twYWtkEx0nX_gVjc4UeUHnRjMAqS12XVsisd3hCkMNS30AvOryxe_OrJn_zGzmnCOOBwgu24aYft4HuXKkrkh3obFOrOLEZUYVOsZ9fk6P_AEWg
def oauth2_sign_in(token):
    try:
        response = id_token.verify_oauth2_token(token, requests.Request())
        email = response.get('email')
        password = make_password(str(email).split("@")[0])
        first_name = response.get('given_name')
        last_name = response.get('family_name')
        user = User.objects.filter(email=email).first()
        if not user:
            user = User.objects.create(email=email, first_name=first_name, last_name=last_name, password=password)
        return get_tokens_for_user(user)
    except ValueError:
        raise AuthenticationFailed("Bad token Google", status.HTTP_403_FORBIDDEN)
