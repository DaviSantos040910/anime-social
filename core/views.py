from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, ProfileForm
from .models import Profile
from django.db.models import Q
from .models import Post 
from django.http import JsonResponse
from .models import Post


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'core/login.html', {'error': 'Usuário ou senha incorretos'})
    
    return render(request, 'core/login.html')


def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'core/cadastro.html', {'error': 'Nome de usuário já existe'})
            elif User.objects.filter(email=email).exists():
                return render(request, 'core/cadastro.html', {'error': 'Email já cadastrado'})
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'core/cadastro.html', {'error': 'As senhas não coincidem'})
    return render(request, 'core/cadastro.html')


@login_required
def home_view(request):
    return render(request, 'core/home.html')


@login_required
def perfil_view(request, username):
    usuario = get_object_or_404(User, username=username)
    posts = usuario.posts.all().order_by('-criado_em')
    return render(request, 'core/perfil.html', {'usuario': usuario, 'posts': posts})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def editar_perfil_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            
            # Verifica se o usuário marcou para remover o avatar
            if request.POST.get('remover_avatar') == 'true':
                if profile.avatar:
                    profile.avatar.delete(save=False)  # Deleta o arquivo do sistema
                profile.avatar = None  # Limpa o campo do modelo

            profile_form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('editar_perfil')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'core/editar_perfil.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def buscar(request):
    query = request.GET.get('q', '')
    resultados = []

    if query:
        resultados = Post.objects.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query)
        ).order_by('-criado_em')

    return render(request, 'core/buscar.html', {'query': query, 'resultados': resultados})


@login_required
def nova_postagem(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        imagem = request.FILES.get('imagem')

        if titulo and imagem:
            Post.objects.create(
                usuario=request.user,
                titulo=titulo,
                descricao=descricao,
                imagem=imagem
            )
            return redirect('perfil', username=request.user.username)

        messages.error(request, 'Título e imagem são obrigatórios.')

    return render(request, 'core/nova_postagem.html')

from django.http import JsonResponse

@login_required
def curtir_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        if request.user in post.curtidas.all():
            post.curtidas.remove(request.user)
            curtido = False
        else:
            post.curtidas.add(request.user)
            curtido = True

        return JsonResponse({
            'curtido': curtido,
            'total_curtidas': post.total_curtidas()
        })
    return JsonResponse({'erro': 'Requisição inválida.'}, status=400)

def buscar_ajax(request):
    termo = request.GET.get('q', '').strip()
    posts = Post.objects.filter(titulo__icontains=termo)[:10]
    usuarios = User.objects.filter(username__icontains=termo)[:10]

    postagens_resultado = [
        {
            'id': p.id,
            'titulo': p.titulo,
            'descricao': p.descricao[:80],
            'imagem': p.imagem.url,
            'usuario': p.usuario.username,
            'total_curtidas': p.total_curtidas,
        } for p in posts
    ]

    usuarios_resultado = [
        {
            'id': u.id,
            'username': u.username,
        } for u in usuarios
    ]

    return JsonResponse({
        'postagens': postagens_resultado,
        'usuarios': usuarios_resultado,
    })