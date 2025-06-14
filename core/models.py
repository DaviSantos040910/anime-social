from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='postagens/')
    criado_em = models.DateTimeField(auto_now_add=True)
    curtidas = models.ManyToManyField(User, related_name='curtidas', blank=True)

    def __str__(self):
        return f"{self.titulo} por {self.usuario.username}"

    def total_curtidas(self):
        return self.curtidas.count()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
