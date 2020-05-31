import graphene
from graphene_django import DjangoObjectType
from .models import posts
from django.contrib.auth import get_user_model

class postsTybe(DjangoObjectType):
    class Meta:
        model = posts

class UserTybe(DjangoObjectType):
    class Meta :
        model = get_user_model()

class Query(graphene.ObjectType):
    posts = graphene.List(postsTybe)

    me = graphene.Field(UserTybe)
    users = graphene.List(UserTybe)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user


    def resolve_posts(self, info,**kwargs):
        return posts.objects.all()

class Createposts(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    body = graphene.String()

    #2
    class Arguments:
        title = graphene.String()
        body = graphene.String()

    #3
    def mutate(self, info, title, body):
        post = posts(title=title, body=body)
        post.save()

        return Createposts(
            id=post.id,
            title=post.title,
            body=post.body,
        )



### USERS

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserTybe)


    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            email = email,
            username = username,
            password = password,
        )
        user.set_password(password)
        user.save()
        return CreateUser(user)


class Mutation(graphene.ObjectType):
    create_posts = Createposts.Field()
    create_user = CreateUser.Field()