        document.addEventListener('DOMContentLoaded', function() {
            fetch('static/matriz.json')
                .then(response => response.json())
                .then(data => {
                    console.log('Dados recebidos do JSON:', data); // Log para verificar os dados

                    const obrigatorias = data.matriz.filter(disciplina => disciplina.obrigatoria == 1);
                    const semestre = {};
                    const form = document.getElementById('disciplinasForm');
                    
                    obrigatorias.forEach(disciplina => {
                        if (!semestre[`semestre${disciplina.semestre}`]) {
                            semestre[`semestre${disciplina.semestre}`] = document.createElement('div');
                            semestre[`semestre${disciplina.semestre}`].className = 'semestre';
                            semestre[`semestre${disciplina.semestre}`].id = `semestre${disciplina.semestre}`;
                            semestre[`semestre${disciplina.semestre}`].innerHTML = `<h3>${disciplina.semestre}º Período </h3>`;
                            document.getElementById('disciplinasForm').appendChild(semestre[`semestre${disciplina.semestre}`]);
                        }
                        const disc = document.createElement('label')
                        disc.className = 'item-disciplina'

                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.name = 'disciplina';
                        checkbox.className = 'checkbox'
                        checkbox.value = disciplina.codigo;

                        const check = document.createElement('span')
                        check.className = 'checkbox-span'

                        const link = document.createElement('a');
                        link.href = `#${disciplina.codigo}`;
                        link.textContent = `${disciplina.nome}`;

                        disc.appendChild(checkbox)
                        disc.appendChild(check)
                        disc.appendChild(link)
                        semestre[`semestre${disciplina.semestre}`].appendChild(disc);
                    });

                    const btn = document.createElement('button');
                    btn.type = 'submit';
                    btn.textContent = 'Gerar sugestão';
                    form.appendChild(btn); 

                    form.addEventListener('submit', function(event) {
                        event.preventDefault();
                        obrigatorias.forEach(disciplina => {
                            const checkbox = form.querySelector(`input[name="disciplina"][value="${disciplina.codigo}"]`);
                            if (checkbox.checked) {
                                disciplina.pago = 1;
                            } else {
                                disciplina.pago = 0;
                            }
                        });
                        const semestre = document.getElementById('tipo-semestre').value

                        const updateJson = { 
                            matriz: obrigatorias,
                            semestre: semestre
                        };
                        console.log(JSON.stringify(updateJson, null, 2)); // Log para verificar updateJson
                        fetch('/processar', {
                            method: 'POST',
                            headers: {
                                'Content-type': 'application/json'
                            },
                            body: JSON.stringify(updateJson)
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log('Resposta do servidor:', data); // Log para verificar a resposta do servidor

                            // Exibir os dados da resposta no HTML
                            const respostaServidor = document.getElementById('respostaServidor');
                            respostaServidor.innerHTML = ''; // Limpa conteúdo anterior
                            const principal = document.createElement('div')
                            if (data) { // Verifique se data não é null
                                data.forEach(grupo => {
                                const lista = document.createElement('ol');
                                    grupo.forEach(disciplinas =>{
                                        const listaDisciplina = document.createElement('li');
                                        const innerList = document.createElement('ul')
                                        innerList.className = 'item-semestre'
                                        disciplinas.forEach( disciplina =>{
                                            const disciplinaItem = document.createElement('li');
                                            disciplinaItem.textContent = disciplina;
                                            innerList.appendChild(disciplinaItem);
                                            disciplinaItem.className = 'item-semestre-disciplina'
                                        });
                                        listaDisciplina.appendChild(innerList);
                                        lista.appendChild(listaDisciplina);
                                    });
                                    const content = document.createElement('div')
                                    content.className = 'container-semestre-item'
                                    content.appendChild(lista)
                                    principal.appendChild(content)
                                });
                                respostaServidor.appendChild(principal);
                            } else {
                                console.error('Dados do servidor são null:', data); // Log de erro se data for null
                            }
                        })
                        .catch(error => console.error('Erro na requisição:', error));
                    });
                })
                .catch(error => console.error('Erro ao buscar os dados:', error));
        });

