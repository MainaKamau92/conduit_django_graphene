create_comment_mutation = '''
mutation {{
  createComment(slug: "{slug}", body: "{body}"){{
    message
    comment {{
      id
      article{{
        slug
      }}
    }}
  }}
}}
'''
update_comment_mutation = '''
mutation {{
  updateComment(id: {id}, body: "{body}"){{
    message
    comment {{
      body
      article{{
        slug
      }}
    }}
  }}
}}
'''

delete_comment_mutation = '''
mutation {{
  deleteComment(id: {id}){{
    message
  }}
}}
'''
get_all_comments_for_article = '''
{{
  articleComments(slug: "{slug}"){{
    id
    body
  }}
}}
'''
