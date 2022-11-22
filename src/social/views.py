from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from users.models import User
from .models import *
from backend.decorators import token_required
from .serializers import PostCreationSerializer, PostSerializer


import uuid, datetime, json

# Create your views here.
class FollowService:
    @api_view(('POST',))
    @staticmethod
    @token_required
    def follow_user(request, user_data, user_to_follow):
        print(user_data)
        user_to_follow_details = User.objects.get(id=user_to_follow)
        if not user_to_follow_details:
            return Response({"message": 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        follow_instance_check = Follow.objects.filter(
            user_followed=int(user_to_follow),
            user_who_followed=int(user_data['user_id'])
        )
        if not follow_instance_check:
            follow_instance = Follow.objects.create(
                user_followed=int(user_to_follow),
                user_who_followed=int(user_data['user_id'])
            )
            
            follow_instance.save()
        
        return Response({"message": 'User followed'}, status=status.HTTP_200_OK)
    
    @api_view(('POST',))
    @staticmethod
    @token_required
    def unfollow_user(request, user_data, user_to_unfollow):
        user_to_unfollow_details = User.objects.get(id=user_to_unfollow)
        if not user_to_unfollow_details:
            return Response({"message": 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        follow_instance = Follow.objects.filter(
            user_followed=user_to_unfollow,
            user_who_followed=user_data['user_id']
        )
        
        follow_instance.delete()
        
        return Response({"message": "User unfollowed"}, status=status.HTTP_200_OK)
    
class LikeService:
    @api_view(('POST',))
    @staticmethod
    @token_required
    def like_post(request, user_data, post_id):
        print(post_id)
        post_details = Post.objects.get(id=post_id)
        if not post_details:
            return Response({"message": 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        post_instance_exists = Likes.objects.filter(
                post_id=post_id,
                user_who_liked=user_data['user_id']
            )
        if not post_instance_exists:
            post_instance = Likes.objects.create(
                post_id=post_id,
                user_who_liked=user_data['user_id']
            )
            post_details.likes_count = post_details.likes_count + 1
            post_instance.save()
            post_details.save()
        
        return Response({"message": "Post liked"}, status=status.HTTP_200_OK)
    
    @api_view(('POST',))
    @staticmethod
    @token_required
    def unlike_post(request, user_data, post_id):
        post_details = Post.objects.get(id=post_id)
        if not post_details:
            return Response({"message": 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        post_instance = Likes.objects.filter(
            post_id=post_id,
            user_who_liked=user_data['user_id']
        )
        
        if post_instance:
            post_details.likes_count = post_details.likes_count - 1
            post_instance.delete()
            post_details.save()
        
        return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)
    
class CommentService:
    @api_view(('POST',))
    @staticmethod
    @token_required
    def add_comment(request, user_data, post_id):
        data = json.loads(request.body.decode('utf-8'))
        post_details = Post.objects.get(id=post_id)
        if not post_details:
            return Response({"message": 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        comment_id = str(uuid.uuid4())
        if post_details.comments is None:
            post_details.comments = {
                'comments': [
                    {
                        "comment_id": comment_id,
                        "commented_by": user_data['user_id'],
                        "comment_text": data.get('comment_text', None),
                        "comment_timestamp": str(datetime.datetime.now() )                       
                    }
                ]
            }
        else:
            post_details.comments['comments'].append({
                "comment_id": comment_id,
                "commented_by": user_data['user_id'],
                "comment_text": data.get('comment_text', None),
                "comment_timestamp": str(datetime.datetime.now())
            })
        post_details.comments_count = post_details.comments_count + 1
        post_details.save()
        data = {
            "message": "Comment added",
            "comment_id": str(comment_id)
        }
        return Response(data, status=status.HTTP_200_OK)
        
    
class PostUtils:
    @api_view(('POST',))
    @staticmethod
    @token_required
    def add_post(request, user_data):
        data = json.loads(request.body.decode('utf-8'))
        if 'title' not in data.keys():
            return Response({"message": "Post title missing"}, status=status.HTTP_400_BAD_REQUEST)
        post_instance = Post.objects.create(
            title=data.get('title', None),
            description=data.get('description', None),
            user_id=user_data['user_id'],
            likes_count=0,
            comments_count=0,
            comments=None
        )
        post_instance.save()
        post_instance = PostCreationSerializer(post_instance)
        return Response(post_instance.data, status=status.HTTP_200_OK)
    
    @api_view(('GET',))
    @staticmethod
    @token_required
    def post_details(request, user_data, post_id):
        post_details = Post.objects.get(id=post_id)
        if not post_details:
            return Response({"message": 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        post_details = PostCreationSerializer(post_details)
        return Response(post_details.data, status=status.HTTP_200_OK)
        
    @api_view(('GET',))
    @staticmethod
    @token_required
    def all_posts(request, user_data):
        posts = Post.objects.all()
        post_details = PostSerializer(posts, many=True)
        return Response(post_details.data, status=status.HTTP_200_OK)
    
    @api_view(('DELETE',))
    @staticmethod
    @token_required
    def delete_post(request, user_data, post_id):
        post_details = Post.objects.get(id=post_id)
        if not post_details:
            return Response({"message": 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if post_details.user_id != user_data['user_id']:
            return Response({"message": 'Only the post author can delete a post'}, status=status.HTTP_403_FORBIDDEN)
            
        
        if post_details.user_id != user_data['user_id']:
            return Response({"message": 'Post can be deleted only by its owner'}, status=status.HTTP_403_FORBIDDEN)
        
        post_details.delete()
        
        return Response({"message": "Post deleted"}, status=status.HTTP_200_OK)