from rest_framework import serializers
from .models import Profile, Post


# ---------- PROFILE ----------
class ProfileSerializer(serializers.ModelSerializer):
    username       = serializers.ReadOnlyField(source="user.username")
    email          = serializers.ReadOnlyField(source="user.email")

    date_of_birth  = serializers.SerializerMethodField()
    gender         = serializers.SerializerMethodField()

    class Meta:
        model  = Profile
        fields = [
            "id", "username", "email",
            "display_name", "bio",
            "date_of_birth", "gender",
            "avatar", "cover", "updated_at",
        ]
        read_only_fields = ["id", "username", "email", "updated_at"]

    def get_date_of_birth(self, obj):
        dob = getattr(obj.user.profile, "date_of_birth", None)
        return dob.isoformat() if dob else None

    def get_gender(self, obj):
        return getattr(obj.user.profile, "gender", None)


from rest_framework import serializers
from .models import Profile, Post

# … ProfileSerializer sin cambios …

# ---------- POST ----------
class PostSerializer(serializers.ModelSerializer):
    author  = serializers.SerializerMethodField()

    # Nombre que usa el frontend → se guarda en el campo text
    content = serializers.CharField(
        source="text",
        allow_blank=True,
        required=False,
    )

    image = serializers.ImageField(required=False, allow_null=True, use_url=True)
    video = serializers.FileField(required=False, allow_null=True, use_url=True)

    class Meta:
        model  = Post
        fields = ["id", "author", "content", "image", "video", "created_at"]

    def get_author(self, obj):
        prof = obj.author.finca_profile
        return {
            "username"    : obj.author.username,
            "display_name": prof.display_name or obj.author.username,
            "avatar"      : prof.avatar.url if prof.avatar else None,
        }
