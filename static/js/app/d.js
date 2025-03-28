async function decryptApi() {
                try {
                    const element1 = document.getElementById("messageId3")
                    const alertDiv1 = document.createElement('div');
                    alertDiv1.className = 'spinner-border text-danger';
                    alertDiv1.role = 'status';
                    alertDiv1.textContent = "";
                    element1.appendChild(alertDiv1);
        
                    const private_pem = document.getElementById('privatePem1').value;
                    const encrypted_data = document.getElementById('encrypted_data').value;

                    const formData = new FormData()
                    formData.append("private_pem", private_pem)
                    formData.append("encrypted_data", encrypted_data)
                    
                    const response = await fetch('/api/decryptData/', {
                        method: 'POST',
                        body: formData
                    });
        
                    const result = await response.json();
                    
                    if (result.status!=="ok") {
                        element1.innerHTML = ""
                        const element = document.getElementById("messageId3")
                        const alertDiv = document.createElement('div');
                        alertDiv.className = 'alert alert-danger';
                        alertDiv.role = 'alert';
                        alertDiv.textContent = "Error";
                        element.appendChild(alertDiv);
                    } else {
                        document.getElementById("plain_text_").value = result.decryptedData
                        element1.innerHTML = ""
                    }
                    
                } catch (error) {
                    console.error('There has been a problem with your fetch operation:', error);
                    document.getElementById('publicPem').value = 'Error: ' + error.message;
                    document.getElementById('privatePem').value = 'Error: ' + error.message;
                }
            }