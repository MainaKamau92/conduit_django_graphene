login_user_query = '''
mutation {{
  loginUser(email:"{email}", password:"{password}"){{
    token
    errors
    success
  }}
}}
'''

register_user_query = '''
mutation {{
  registerUser(username:"{username}" email: "{email}", password: "{password}"){{
    user {{
      email
    }}
    successMessage
    errors
  }}
}}

'''

get_all_users_query = '''
{
  users {
    id
    username
    email
  }
}
'''
get_single_user_query = '''
{{
  user(id:{id}) {{
    id
    username
    email
  }}
}}

'''

get_inexistent_user_query = '''
{
  user(id:400){
    id
    username
  }
}
'''
