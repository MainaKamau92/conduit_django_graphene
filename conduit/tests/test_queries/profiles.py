profile_update_mutation = '''
mutation {{
  updateProfile(bio: "{bio}", name: "{name}", image: "{image}") {{
    profile {{
      bio
      name
      user {{
        username
        email
      }}
    }}
    message
  }}
}}
'''

get_all_profiles = '''
{
  profiles {
    id
    bio
    image
  }
}
'''

get_single_profile = '''
{{
  profile (id: {id}){{
    id
    bio
    image
  }}
}}
'''