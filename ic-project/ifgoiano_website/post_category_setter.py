from post import Post


class PostCategorySetter:
    @staticmethod
    def set(post: Post):
        post.category = 'unknown'
