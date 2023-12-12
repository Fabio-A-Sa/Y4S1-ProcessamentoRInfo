// imports
const express = require("express");
const path = require("path");
const app = express();
const cors = require("cors");
const fs = require("fs");

// paths
const cssPath = path.join(__dirname, "css");
const jsPath = path.join(__dirname, "js");
const htmlPath = path.join(__dirname, "html");

// constants
let LOCATIONS;
const HOTELS_LIMIT = 20;
const REVIEWS_LIMIT = 20;
const SAVE_MLT_RESULTS = false;
const PORT = process.argv[2] || 3000;

const CONFIG = {
    query: {
        endpoint: "http://localhost:8983/solr/hotels/select?",
        parameters: {
            indent: "true",
            "q.op": "AND",
            sort: "score desc",
            start: "0",
            rows: "100",
            fl: "*, [child]",
            defType: "edismax",
            qf: "text^7 name location^2",
            pf: "text^10",
            ps: 3,
        },
    },
    mlt: {
        endpoint: "http://localhost:8983/solr/hotels/mlt?",
        results: "../evaluation/mlt/results.json",
        parameters: {
            "mlt.fl": "text",
            "mlt.mintf": "2",
            "mlt.mindf": "5",
            sort: "score desc",
            start: "0",
            rows: "10",
        },
    },
};

const RANGES = ["rrmin", "rrmax", "hrmin", "hrmax"];

// pages
const baseStructure = fs.readFileSync(
    path.join(htmlPath, "base-page.html"),
    "utf8"
);
const homePage = baseStructure
    .replace(
        "<main></main>",
        fs.readFileSync(path.join(htmlPath, "home-page.html"), "utf8")
    )
    .replace("<locations></locations>", selectLocations());
const searchPage = baseStructure
    .replace(
        "<main></main>",
        fs.readFileSync(path.join(htmlPath, "search-page.html"), "utf8")
    )
    .replace("<locations></locations>", selectLocations());
const hotelPage = baseStructure.replace(
    "<main></main>",
    fs.readFileSync(path.join(htmlPath, "hotel-page.html"), "utf8")
);
const morePage = baseStructure.replace(
    "<main></main>",
    fs.readFileSync(path.join(htmlPath, "more-page.html"), "utf8")
);

// dependencies
app.use(cors());
app.use((_, res, next) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader(
        "Access-Control-Allow-Methods",
        "GET, POST, OPTIONS, PUT, PATCH, DELETE"
    );
    res.setHeader(
        "Access-Control-Allow-Headers",
        "X-Requested-With,content-type"
    );
    res.setHeader("Access-Control-Allow-Credentials", true);
    next();
});
app.use("/css", express.static(cssPath, { extensions: ["css"] }));
app.use("/js", express.static(jsPath, { extensions: ["js"] }));
app.use(express.static(htmlPath));

// Fetch the response of a request
async function getResponse(request) {
    const response = await fetch(request);
    if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
    }
    return await response.json();
}

// Fetch reviews based on search inputs
async function getReviews(params, limit = REVIEWS_LIMIT) {
    // Filter: location
    const queryLocation =
        `&fq={!child of=\"*:* -_nest_path_:*\"}location:` +
        (params.location && params.location !== "Any"
            ? params.location.split(" ")[0]
            : "*");

    // Filter: common parameters
    const request = `${CONFIG.query.endpoint}q=${
        params.input
    }&${new URLSearchParams(CONFIG.query.parameters)}${queryLocation}`;
    let reviews = (await getResponse(request)).response.docs;

    // Filter: review rate
    if (params.rrmin && params.rrmax && params.rrmin <= params.rrmax) {
        reviews = reviews.filter(
            (review) =>
                review.rate <= params.rrmax && review.rate >= params.rrmin
        );
    }

    // Filter: hotel average rate
    if (params.hrmin && params.hrmax && params.hrmin <= params.hrmax) {
        const hotelRates = await Promise.all(
            reviews.map(async (review) => {
                const hotelRate = (await getHotelInfo(review.id.split("/")[0]))
                    .average_rate[0];
                return { review, hotelRate };
            })
        );

        reviews = hotelRates
            .map(({ review, hotelRate }) => {
                if (hotelRate >= params.hrmin && hotelRate <= params.hrmax)
                    return review;
            })
            .filter((review) => review);
    }

    // Limitation
    return reviews.length <= limit ? reviews : reviews.slice(0, limit);
}

// Fetch hotels with a specified limit
async function getHotels(limit = HOTELS_LIMIT) {
    const request = `${CONFIG.query.endpoint}q=name:*&rows=${limit}&sort=average_rate%20desc`;
    return (await getResponse(request)).response.docs;
}

// Fetch all unique locations
async function getLocations() {
    try {
        const locationsContent = fs.readFileSync(
            "./assets/locations.json",
            "utf8"
        );
        LOCATIONS = JSON.parse(locationsContent);
    } catch (error) {
        const hotels = await getHotels(30000);
        const locationsSet = new Set(hotels.map((h) => h.location));
        LOCATIONS = Array.from(locationsSet).sort();

        fs.writeFile(
            "./assets/locations.json",
            JSON.stringify(locations, null, 2),
            (err) => {
                if (err) throw err;
            }
        );
    }
}

// Fetch hotel information based on ID
async function getHotelInfo(hotelId) {
    const request = `${CONFIG.query.endpoint}q=id:${hotelId}&rows=1`;
    return (await getResponse(request)).response.docs[0];
}

// Fetch review information based on ID
async function getReview(reviewId) {
    const request = `${CONFIG.query.endpoint}${new URLSearchParams({
        rows: 1,
        q: `id:${reviewId}`,
    })}`;
    return (await getResponse(request)).response.docs[0];
}

// Fetch reviews of a hotel based on ID
async function getHotelReviews(hotelId, limit = REVIEWS_LIMIT) {
    const request = `${CONFIG.query.endpoint}q=id:${hotelId}/*&rows=${limit}`;
    const reviews = (await getResponse(request)).response.docs;
    return reviews.length <= limit ? reviews : reviews.slice(0, limit);
}

// Transforms specified query tokens in a given text into bold format.
function transformText(text, query) {
    const wordsInText = text.split(/\b/);
    const wordsInQuery = query.toLowerCase().split(/\b/);

    const transformedWords = wordsInText.map((word) => {
        const cleanedWord = word.replace(/[^a-zA-ZÀ-ÿ0-9]/g, "");
        return wordsInQuery.includes(cleanedWord.toLowerCase())
            ? `<b>${word}</b>`
            : word;
    });

    return transformedWords.join("");
}

// Create HTML for reviews
async function createReviewsHTML(docs, showHotel, query = null) {
    const articlesHTML = await Promise.all(
        docs.map(async (doc) => {
            const hotelId = doc.id.split("/")[0];
            const reviewId = doc.id.split("#")[1];
            const hotel = await getHotelInfo(hotelId);
            const text = query ? transformText(doc.text, query) : doc.text;
            const hotelInfoHTML = showHotel
                ? `<h3><a href="/hotel?id=${hotelId}">${hotel.name}</a> with ${hotel.average_rate} stars in ${hotel.location}</h3>`
                : "";
            return `
            <article class="review">
                ${hotelInfoHTML}
                <h4>"${text}"</h4>
                <h5>${doc.date}. Rate: ${doc.rate} stars</h5>
                <h6><a href="/more?hotelId=${hotelId}&reviewId=${reviewId}">More...</a></h6>
            </article>
        `;
        })
    );

    const header = `<h3 class="left">${docs.length} ${
        showHotel ? "results" : "reviews"
    }:</h3>`;
    return docs.length !== 0 ? header + articlesHTML.join("") : null;
}

// Create HTML for selecting hotels location
function selectLocations() {
    getLocations();
    let htmlString =
        '<select name="location" id="location"><option value="Any" selected>Any</option>';
    LOCATIONS.forEach((location) => {
        htmlString += `<option value="${location}">${location}</option>`;
    });
    return htmlString + "</select>";
}

// Create HTML for a single hotel
function createHotelHTML(hotel, hotelPage) {
    return `
        <article class="${hotelPage ? "" : "hotel"}">
            <h3><a href="/hotel?id=${hotel.id}">${hotel.name}</a></h3>
            <h4>${hotel.average_rate} stars, in ${hotel.location}</h4>
        </article>
    `;
}

// Create HTML for multiple hotels
function createHotelsHTML(hotels) {
    let hotelsHTML = "";
    hotels.forEach((hotel) => {
        hotelsHTML += createHotelHTML(hotel, false);
    });
    return hotelsHTML;
}

// Update the search page with results and search inputs
function getUpdatedSearchPage(reviews, params) {
    let updatedHTML = searchPage;

    // Update input
    if (params.input)
        updatedHTML = updatedHTML.replace(
            /id="searchInput"/g,
            `id="searchInput" value="${params.input}"`
        );

    // Update location
    if (params.location && params.location !== "Any") {
        updatedHTML = updatedHTML
            .replace(
                '<option value="Any" selected="">Any</option>',
                '<option value="Any">Any</option>'
            )
            .replace(
                `<option value="${params.location}">${params.location}</option>`,
                `<option value="${params.location}" selected="">${params.location}</option>`
            );
    }

    const ranges = {
        hrmin: 0,
        hrmax: 5,
        rrmin: 0,
        rrmax: 5,
    };

    // Update ranges
    RANGES.forEach((range) => {
        if (params[range]) ranges[range] = params[range];
    });

    Array("hrmin", "rrmin").forEach((range) => {
        updatedHTML = updatedHTML.replace(
            `<input id="${range}" type="range" class="range-min" min="0" max="5" value="0" step="1" />`,
            `<input id="${range}" type="range" class="range-min" min="0" max="5" value="${ranges[range]}" step="1" />`
        );
    });
    Array("hrmax", "rrmax").forEach((range) => {
        updatedHTML = updatedHTML.replace(
            `<input id="${range}" type="range" class="range-max" min="0" max="5" value="5" step="1" />`,
            `<input id="${range}" type="range" class="range-max" min="0" max="5" value="${ranges[range]}" step="1" />`
        );
    });

    // Update reviews
    if (reviews)
        updatedHTML = updatedHTML.replace("<p>No results found</p>", reviews);

    return updatedHTML;
}

// Update the hotel page with hotel information and reviews
function getUpdatedHotelPage(hotel, reviews) {
    let updatedHTML = hotelPage;
    if (hotel)
        updatedHTML = updatedHTML.replace(
            "<p>No hotel found</p>",
            createHotelHTML(hotel, true)
        );
    if (reviews)
        updatedHTML = updatedHTML.replace("<p>No reviews found</p>", reviews);
    return updatedHTML;
}

// Update the more page with review and more reviews information
function getUpdatedMorePage(review, moreReviews) {
    let updatedHTML = morePage;
    if (review)
        updatedHTML = updatedHTML.replace(
            "<p>No review found</p>",
            `<h4>"${review.text}"</h4>`
        );
    if (moreReviews)
        updatedHTML = updatedHTML.replace(
            "<p>No related reviews found</p>",
            moreReviews
        );
    return updatedHTML;
}

// More like this results
async function moreLikeThis(review) {
    const request = `${CONFIG.mlt.endpoint}${
        CONFIG.mlt.parameters
    }&${new URLSearchParams({
        q: `id:${review.id}`,
    })}`;
    const docs = (await getResponse(request)).response.docs;

    // Save results for evaluation
    if (SAVE_MLT_RESULTS && docs.length === 10) {
        let results;

        try {
            const resultsFile = fs.readFileSync(CONFIG.mlt.results, "utf8");
            results = JSON.parse(resultsFile);
        } catch (error) {
            results = [];
        }

        results.push({
            review: review.text,
            related: docs.map((doc) => doc.text),
        });

        fs.writeFile(
            CONFIG.mlt.results,
            JSON.stringify(results, null, 2),
            (err) => {
                if (err) throw err;
            }
        );
    }

    return docs;
}

// Home page
app.get("/", async (req, res) => {
    const hotels = await getHotels();
    const html = hotels
        ? homePage.replace("<p>No hotels found</p>", createHotelsHTML(hotels))
        : homePage;
    res.send(html);
});

// Search page
app.get("/search", async (req, res) => {
    const input = req?.query?.input;
    const location = req?.query?.location;
    const params = {
        input: input,
        location: location,
        rrmin: req?.query?.rrmin,
        rrmax: req?.query?.rrmax,
        hrmin: req?.query?.hrmin,
        hrmax: req?.query?.hrmax,
    };
    const reviews = await getReviews(params);
    const reviewsHTML = await createReviewsHTML(reviews, true, input);
    const updatedHTML = getUpdatedSearchPage(reviewsHTML, params);
    res.send(updatedHTML);
});

// Hotel page
app.get("/hotel", async (req, res) => {
    const id = req?.query?.id;
    const results = await getHotelReviews(id);
    const hotel = await getHotelInfo(id);
    const reviewsHTML = await createReviewsHTML(results, false);
    const updatedHTML = getUpdatedHotelPage(hotel, reviewsHTML);
    res.send(updatedHTML);
});

// More like this page
app.get("/more", async (req, res) => {
    const hotelId = req?.query?.hotelId;
    const reviewId = req?.query?.reviewId;
    const review = await getReview(`${hotelId}/reviews#${reviewId}`);
    const moreReviews = await moreLikeThis(review);
    const moreReviewsHTML = await createReviewsHTML(moreReviews, true);
    const updatedHTML = getUpdatedMorePage(review, moreReviewsHTML);
    res.send(updatedHTML);
});

app.use(express.static(__dirname + "/public"));

// Create server
app.listen(PORT, () => {
    console.log(`Server listening at http://localhost:${PORT}`);
});
