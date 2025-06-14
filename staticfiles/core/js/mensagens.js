document.addEventListener('DOMContentLoaded', function () {
  // Mensagens temporárias
  const messages = document.querySelectorAll('.message');
  messages.forEach(msg => {
    msg.classList.add('show');
    setTimeout(() => {
      msg.classList.remove('show');
      msg.style.display = 'none';
    }, 4000); // 4 segundos
  });

  // Preview e remoção do avatar
  const input = document.querySelector('input[name="avatar"]');
  const preview = document.getElementById('avatar-preview');
  const removeBtn = document.getElementById('remove-avatar');
  const removerInput = document.getElementById('remover-avatar-input');

  if (input && preview) {
    input.addEventListener('change', function (e) {
      const file = e.target.files[0];
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function (event) {
          preview.src = event.target.result;
          preview.style.display = 'block';
          if (removeBtn) removeBtn.style.display = 'inline-block';
          if (removerInput) removerInput.value = 'false';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  if (removeBtn && preview && removerInput) {
    removeBtn.addEventListener('click', function () {
      input.value = ''; // limpa o input de arquivo
      preview.src = '';
      preview.style.display = 'none';
      removeBtn.style.display = 'none';
      removerInput.value = 'true'; // indica ao backend que o avatar deve ser removido
    });
  }
});
