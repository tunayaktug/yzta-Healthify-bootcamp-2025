console.log("✅ script.js yüklendi!");
const catDropdown = document.getElementById('categoryDropdown');
if (catDropdown) {
  catDropdown.addEventListener('change', function() {
    const selected = this.value;
    if (selected !== "Kategori Seçin") {
      window.location.href = `/upload.html?category=${selected}`;
    }
  });
}

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

  document.querySelectorAll('.dot').forEach(dot => dot.classList.remove('active'));
  document.querySelectorAll('.dot')[index].classList.add('active');
}

setInterval(() => {
  currentIndex = (currentIndex + 1) % testimonials.length;
  showTestimonial(currentIndex);
}, 6000);

document.getElementById('loginBtn').addEventListener('click', function () {
  window.location.href = "login.html";
});

showTestimonial(0);

// ✅ GÜNCEL HABERLERİ ÇEK
document.addEventListener("DOMContentLoaded", () => {
  const newsSection   = document.getElementById('news-section');
  const newsContainer = document.getElementById('news-container');

  // Ok butonları oluştur
  const prevBtn = document.createElement('button');
  prevBtn.className = 'news-nav prev';
  prevBtn.textContent = '‹';
  const nextBtn = document.createElement('button');
  nextBtn.className = 'news-nav next';
  nextBtn.textContent = '›';
  newsSection.append(prevBtn, nextBtn);

  prevBtn.addEventListener('click', () => {
    newsContainer.scrollBy({ left: -newsContainer.clientWidth * 0.8, behavior: 'smooth' });
  });
  nextBtn.addEventListener('click', () => {
    newsContainer.scrollBy({ left:  newsContainer.clientWidth * 0.8, behavior: 'smooth' });
  });

  // API'den haberleri çek
  fetch("http://localhost:8000/news")
    .then(res => res.json())
    .then(data => {
      const articles = data.results;
      if (!Array.isArray(articles) || articles.length === 0) {
        newsContainer.innerHTML = "<p>Haber bulunamadı.</p>";
        return;
      }
      // Kartları oluştur
      let count = 0;
      for (let i = 0; i < articles.length && count < 10; i++) {
        const article = articles[i];
        const title = article.title || "Başlık yok";
        const link = article.link || "#";
        const desc = (article.description || "").replace(/<[^>]+>/g, '').slice(0, 100) + "…";
        const img = article.image_url;
        // Fotoğrafı olmayan, boş veya hatalı url'li haberleri atla
        if (!img || img.trim() === '' || img.startsWith('<')) continue;

        const card = document.createElement("a");
        card.href = link;
        card.target = "_blank";
        card.className = "news-card";
        card.innerHTML = `
          <img src="${img}" alt="${title}">
          <div class="news-card-content">
            <h3>${title}</h3>
            <p>${desc}</p>
          </div>
        `;
        // Görsel yüklenemezse kartı kaldır
        const imgEl = card.querySelector('img');
        imgEl.onerror = () => { card.remove(); };
        newsContainer.append(card);
        count++;
      }
    })
    .catch(err => {
      console.error("❌ Hata:", err);
      newsContainer.innerHTML = "<p>Haberler yüklenemedi.</p>";
    });
});
