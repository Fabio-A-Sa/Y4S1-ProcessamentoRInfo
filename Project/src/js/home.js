load = () => {
    const hotelCards = document.querySelectorAll(
        "section.hotels article.hotel"
    );

    hotelCards.forEach((card) => {
        card.addEventListener("click", () => {
            card.querySelector("a")?.click();
        });
    });
};

load();
