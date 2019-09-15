create_article_mutation = '''
mutation {{
  createArticle(title: "{title}", description: "{description}", body: "{body}", tags: ["{lorem}", "{ipsum}"]) {{
    article {{
      id
      slug
      title
      tags {{
        id
        tag
      }}
    }}
    message
  }}
}}
'''
get_all_articles = '''
{
  articles {
    id
    slug
    title
    favoritedBy {
      user {
        username
      }
    }
    author {
      user {
        username
      }
    }
  }
}
'''
get_single_article = '''
{{
  article(slug:"{slug}") {{
    id
    slug
    title
  }}
}}
'''

update_article_mutation = '''
mutation {{
  updateArticle(slug:"{slug}", title:"{title}") {{
    article {{
      id
      slug
      title
    }}
    message
  }}
}}
'''

delete_article_mutation = '''
mutation{{
  deleteArticle(slug:"{slug}"){{
    message
  }}
}}
'''

favorite_article_mutation = '''
mutation{{
  favoriteArticle(slug:"{slug}"){{
    message
    article {{
      id
      slug
      title
      favoritedBy {{
        user {{
          username
        }}
      }}
    }}
  }}
}}
'''
