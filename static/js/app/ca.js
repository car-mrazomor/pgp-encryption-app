async function callApi() {
                try {
                    const element1 = document.getElementById("messageId")
                    const alertDiv1 = document.createElement('div');
                    alertDiv1.className = 'spinner-border text-danger';
                    alertDiv1.role = 'status';
                    alertDiv1.textContent = "";
                    element1.appendChild(alertDiv1);
                    const response = await fetch('/api/generateKeys', {
                        method: 'GET'
                    });

                    const result = await response.json();
    
                    if (result.status!=="ok") {
                        const element = document.getElementById("messageId")
                        const alertDiv = document.createElement('div');
                        alertDiv.className = 'alert alert-warning';
                        alertDiv.role = 'alert';
                        alertDiv.textContent = "Error";
                        element.appendChild(alertDiv);
                        return
                    }
                    
                    document.getElementById('publicPem').value = result.public_pem;
                    document.getElementById('privatePem').value = result.private_pem;
                    element1.innerHTML = ""
                } catch (error) {
                    console.error('There has been a problem with your fetch operation:', error);
                    document.getElementById('publicPem').value = 'Error: ' + error.message;
                    document.getElementById('privatePem').value = 'Error: ' + error.message;
                }
            }