document.getElementById('calcForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        coin_value: parseFloat(document.getElementById('coinValue').value),
        measured_weight: parseFloat(document.getElementById('measuredWeight').value),
        tare_weight: parseFloat(document.getElementById('tareWeight').value)
    };

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || 'Request failed');
        }
        document.getElementById('valueOutput').textContent = result.calculated_value.toFixed(2);
        document.getElementById('countOutput').textContent = result.coin_count;
    } catch (err) {
        document.getElementById('valueOutput').textContent = '-';
        document.getElementById('countOutput').textContent = '-';
        alert(err.message);
    }
});
