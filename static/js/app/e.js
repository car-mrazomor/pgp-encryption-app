async function encryptApi() {
                try {
                    const element1 = document.getElementById("messageId2")
                    const alertDiv1 = document.createElement('div');
                    alertDiv1.className = 'spinner-border text-danger';
                    alertDiv1.role = 'status';
                    alertDiv1.textContent = "";
                    element1.appendChild(alertDiv1);
        
                    const public_pem = document.getElementById('publicPem2').value;
                    const plain_text = document.getElementById('plain_text').value;

                    const formData = new FormData()
                    formData.append("public_pem", public_pem)
                    formData.append("plain_text", plain_text)
                    
                    const response = await fetch('/api/encryptData/', {
                        method: 'POST',
                        body: formData
                    });
        
                    const result = await response.json();
                    
                    if (result.status!=="ok") {
                        element1.innerHTML = ""
                        const element = document.getElementById("messageId2")
                        const alertDiv = document.createElement('div');
                        alertDiv.className = 'alert alert-danger';
                        alertDiv.role = 'alert';
                        alertDiv.textContent = "Error";
                        element.appendChild(alertDiv);
                    } else {
                        document.getElementById("encrypted_data_").value = result.encryptedData
                        element1.innerHTML = ""
                    }
                    
                } catch (error) {
                    console.error('There has been a problem with your fetch operation:', error);
                    document.getElementById('publicPem').value = 'Error: ' + error.message;
                    document.getElementById('privatePem').value = 'Error: ' + error.message;
                }
            }