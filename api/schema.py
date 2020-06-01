import graphene
from graphene_django import DjangoObjectType
from .models import posts
from django.contrib.auth import get_user_model

class UserTybe(DjangoObjectType):
    class Meta :
        model = get_user_model()

class postsTybe(DjangoObjectType):
    # posted_by = graphene.Field(UserTybe)
    class Meta:
        model = posts

class Query(graphene.ObjectType):
    posts = graphene.List(postsTybe,first=graphene.Int(), skip=graphene.Int())

    me = graphene.Field(UserTybe)

    users = graphene.List(UserTybe)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user


    def resolve_posts(self, info, first=None, skip=None,**kwargs):
        qs = posts.objects.all()
        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

class Createposts(graphene.Mutation):
    # id = graphene.Int()
    # title = graphene.String()
    # body = graphene.String()
    # posted_by = graphene.Field(UserTybe)
    post = graphene.Field(postsTybe)

    #2
    class Arguments:
        title = graphene.String()
        body = graphene.String()

    #3
    def mutate(self, info, title, body):
        user = info.context.user
        post = posts(title=title, body=body, posted_by=user)
        post.save()

        # return Createposts(
        #     id=post.id,
        #     title=post.title,
        #     body=post.body,
        #     posted_by = user
        # )
        return Createposts(post)


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