document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("predictForm").addEventListener("submit", async function (event) {
        event.preventDefault();

        let formData = {
            Owner_Type: document.getElementById("Owner_Type").value,
            Mileage: document.getElementById("Mileage").value,
            Engine: document.getElementById("Engine").value,
            Power: document.getElementById("Power").value,
            Seats: document.getElementById("Seats").value,
            New_Price: document.getElementById("New_Price").value,
            depreciation_rate: document.getElementById("depreciation_rate").value,
            car_age: document.getElementById("car_age").value
        };

        console.log("Sending Data:", formData);

        try {
            let response = await fetch("http://127.0.0.1:5500/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            let data = await response.json();
            console.log("Response Received:", data);
            document.getElementById("result").innerText = "Predicted Price: ₹" + data.price;
        } catch (error) {
            console.error("Error Fetching Prediction:", error);
        }
    });
});
