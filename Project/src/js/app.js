async function search() {
    const input = document.querySelector("#searchInput").value;
    const location = document.querySelector("#location").value;
    const reviewRateMin = document.querySelector("#rrmin").value;
    const reviewRateMax = document.querySelector("#rrmax").value;
    const hotelRateMin = document.querySelector("#hrmin").value;
    const hotelRateMax = document.querySelector("#hrmax").value;
    window.location.href = `/search?${new URLSearchParams({
        input: input,
        location: location,
        rrmin: reviewRateMin,
        rrmax: reviewRateMax,
        hrmin: hotelRateMin,
        hrmax: hotelRateMax,
    })}`;
}
