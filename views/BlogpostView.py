from flask import request, json, Response, Blueprint, g
from shared.Authorization import Auth
from models.BlogpostModel import BlogpostModel, BlogpostSchema

blog_post_api = Blueprint('blogposts', __name__)
blog_schema = BlogpostSchema(only=['title', 'contents'])


@blog_post_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Blog posts
    """
    req_data = request.get_json()
    req_data['owner_id'] = g.user.get('id')
    data, error = blog_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    post = BlogpostModel(req_data)
    post.save()
    data = blog_schema.dump(post).data
    return custom_response(data, 201)


@blog_post_api.route('/', methods=['GET'])
def get_all_blogpost():
    """
     Get All Blogposts
     """

    blog_posts = BlogpostModel.get_all_blogposts()
    serialize_posts = blog_schema.dump(blog_posts, many=True).data
    return custom_response(serialize_posts, 200)


@blog_post_api.route('/<int:blogpost_id>', methods=['GET'])
def get_one_post(blogpost_id):
    """
    Get A Blogpost
    """
    post = BlogpostModel.get_one_blogpost(blogpost_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = blog_schema.dump(post).data
    return custom_response(data, 200)


@blog_post_api.route('/<int:blogpost_id>', methods=['PUT'])
@Auth.auth_required
def update(blogpost_id):
    """
    update post
    """

    req_data = request.get_json()

    post = BlogpostModel.get_one_blogpost(blogpost_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = blog_schema.dump(post).data
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    data, error = blog_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    post.update(data)

    data = blog_schema.dump(post).data
    return custom_response(data, 200)


def custom_response(res, status_code):
    """
  Custom Response Function
  """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
