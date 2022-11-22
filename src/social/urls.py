from django.urls import path
from .views import FollowService, PostUtils, CommentService, LikeService

urlpatterns = [
    path('follow/<int:user_to_follow>', FollowService.follow_user, name='Follow user'),
    path('unfollow/<int:user_to_unfollow>', FollowService.unfollow_user, name="Unfollow user"),
    path('post/like/<int:post_id>', LikeService.like_post, name='Like post'),
    path('post/unlike/<int:post_id>', LikeService.unlike_post, name='UnLike post'),
    path('post/comment/<int:post_id>', CommentService.add_comment, name='Add comment'),
    path('post', PostUtils.add_post, name='Add post'),
    path('post/<int:post_id>', PostUtils.post_details, name='Get post details'),
    path('posts/all/', PostUtils.all_posts, name='Get all posts'),
    path('post/del/<int:post_id>', PostUtils.delete_post, name='Delete post'),
]

