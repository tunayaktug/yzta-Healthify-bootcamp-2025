document.getElementById('categoryDropdown').addEventListener('change', function() {
  const selected = this.value;
  if (selected !== "Kategori Seçin") {
    window.location.href = `/upload.html?category=${selected}`;
  }
});

const testimonials = [
  {
    name: "Sarah W.",
    photo: "https://randomuser.me/api/portraits/women/44.jpg",
    comment: "“Harika bir araç! Sağlık yönetimimde bana çok yardımcı oldu.”"
  },
  {
    name: "Ali K.",
    photo: "https://randomuser.me/api/portraits/men/34.jpg",
    comment: "“Çok hızlı ve kullanışlı bir sistem. Kesinlikle öneririm.”"
  },
  {
    name: "Elif T.",
    photo: "https://randomuser.me/api/portraits/women/68.jpg",
    comment: "“Yapay zeka analizi gerçekten etkileyici.”"
  },
  {
    name: "Deniz A.",
    photo: "https://randomuser.me/api/portraits/men/23.jpg",
    comment: "“Görsel yükledikten birkaç saniye sonra net bilgi aldım.”"
  },
  {
    name: "Zeynep B.",
    photo: "https://randomuser.me/api/portraits/women/25.jpg",
    comment: "“Kullanıcı dostu arayüzü çok beğendim.”"
  }
];

let currentIndex = 0;

function showTestimonial(index) {
  currentIndex = index;
  const testimonial = testimonials[index];
  document.querySelector('.user-photo').src = testimonial.photo;
  document.getElementById('userName').textContent = testimonial.name;
  document.getElementById('userComment').textContent = testimonial.comment;

  // Dots
  document.querySelectorAll('.dot').forEach(dot => dot.classList.remove('active'));
  document.querySelectorAll('.dot')[index].classList.add('active');
}

// Otomatik geçiş (opsiyonel)
setInterval(() => {
  currentIndex = (currentIndex + 1) % testimonials.length;
  showTestimonial(currentIndex);
}, 6000); // Her 6 saniyede değişir

document.getElementById('loginBtn').addEventListener('click', function () {
  window.location.href = "login.html";
});
// İlk yükleme
showTestimonial(0);
