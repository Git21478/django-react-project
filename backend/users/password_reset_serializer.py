class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        fields = ["email"]
    
    def validate(self, attrs):
        try:
            email = attrs.get("email", "")
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base_encode(user.id)
                token = PasswordResetTokenGenerator().make_token(user)
            
            return attrs
        except expression as identifier:
            pass
        return super().validate(attrs)

validators=[
    MinLengthValidator(limit_value=1),
    MaxLengthValidator(limit_value=10),
]