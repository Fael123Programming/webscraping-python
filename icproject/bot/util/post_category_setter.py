from icproject.bot.post import Post


class PostCategorySetter:

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(PostCategorySetter, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def set_of(post: Post):
        post.category = 1  # unknown category.
