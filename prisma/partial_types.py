from prisma.models import User, Article, Comment

#relation fieldsを除去したArticleのPartialTypeを作成
Article.create_partial('ArticleExcludeRelationFields', exclude_relational_fields=True)
Comment.create_partial('CommentExcludeRelationFields', exclude_relational_fields=True)