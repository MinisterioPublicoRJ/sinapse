import {
    formatCPF,
    formatCPFOrCNPJ,
    formatCNPJ,
    formatDate,
    formatDocumentHierarchy,
    formatMPRJ,
    get,
} from '/static/js/utils.js'

const DOMINIO = 'http://apps.mprj.mp.br/sistema/dominio'

const titleProperty = {
    documento_personagem: 'nr_mp',
    documento_personagemFn: formatMPRJ,
    embarcacao: 'nome_embarcacao',
    pessoa: 'nome',
    pessoa_juridica: 'razao_social',
    veiculo: 'descricao',
}

/**
 * Creates a card for a doc/entity
 * @param {Object} entity data for this entity
 * @param {String} key the entity type (empresa, pessoa, veiculo)
 * @param {*} data The whole data returned from API, to get highlight information
 * @param {bool} isSearchDetailStep whether the card is being called within the search list result or in the searchDetails screen
 * @param {String} bondSearchUuid UUID of 1st element if bond search
 * @param {String} bondSearchType 1st element type
*/
export const entityCard = (entity, key, data, isSearchDetailStep, bondSearchUuid, bondSearchType) => {
    let onclickFn = `onclick="searchDetailStep('${entity.uuid}', '${key}')"`
    let titleClass = 'col-md-2 text-center container-foto'
    let bodyClass = 'col-md-10'
    let title = `<h3 class="color-${key}">${returnHighlightedProperty(entity, titleProperty[key], data[key].highlighting, titleProperty[key+'Fn'] || null)}</h3>`

    if (isSearchDetailStep) {
        onclickFn = ''
        titleClass = 'col-md-12 text-center title'
        bodyClass = 'col-md-12'
    }
    if (bondSearchUuid) {
        onclickFn = `onclick="doBondSearch('${bondSearchUuid}', '${bondSearchType}', '${entity.uuid}', '${entity.label}')"`
    }

    let ret = `<div class="card-resultado clearfix" ${onclickFn}>
        <div class="${titleClass}">`
    if (key === 'pessoa') {
        pessoaFoto(entity.rg)
        ret += `<img class="pessoa-foto" data-rg="${entity.rg}" src="/static/img/icon/pessoa.svg" />`
    } else {
        ret += `<img src="/static/img/icon/${key}.svg" />`
    }
    ret += `</div>
        <div class="${bodyClass}">
            <div class="row">`
    if (isSearchDetailStep) {
        ret += `
                <div class="col-md-1">
                    <h3 onclick="backToSearch()" style="cursor:pointer">⬅️</h3>
                </div>
                <div class="col-md-10">`
    } else {
        ret += `
                <div class="col-md-12">`
    }
    ret +=          `${title}
                </div> <!-- title-col -->`
    switch(key) {
        case 'documento_personagem':
            ret += documentoCard(entity, data[key].highlighting, isSearchDetailStep)
            break
        case 'embarcacao':
            ret += embarcacaoCard(entity, data[key].highlighting, isSearchDetailStep)
            break
        case 'pessoa_juridica':
            ret += empresaCard(entity, data[key].highlighting, isSearchDetailStep)
            break
        case 'pessoa':
            ret += pessoaCard(entity, data[key].highlighting, isSearchDetailStep)
            break
        case 'veiculo':
            ret += veiculoCard(entity, data[key].highlighting, isSearchDetailStep)
            break
        default:
            // just spit it out
            ret += JSON.stringify(entity)
    }
    ret += `</div> <!-- row -->
        </div> <!-- body -->
    </div> <!-- card-resultado -->`
    return ret
}

// <a href="${DOMINIO}/#/document-search/${doc.nr_mp}" target="_blank" title="Abrir no Domínio">🔗</a>

/**
 * Creates a card for a given document
 * @param {Object} doc a entity document representing a document
 * @param {String} doc.cldc_ds_hierarquia Information about document hierarchy, separated with |, first level is all caps
 * @param {String[]} doc.ds_info_personagem Array of personagens
 * @param {String} doc.dt_cadastro Date of creation
 * @param {String} doc.nr_externo External Number
 * @param {String} doc.nr_mp MP Number
 * @param {Object} highlighting highlighted terms returned by search
 * @param {Object} highlighting.uuid a object that has a highlighted term
 * @param {String[]} highlighting.uuid.prop the terms that matches the searched term
 */
const documentoCard = (doc, highlighting) => {
    return `
        <div class="body col-md-12">
            <div class="row">
                <dl>
                    <div class="col-md-6">
                        <dt>Classe</dt>
                        <dd class="color-documento">${returnHighlightedProperty(doc, 'cldc_ds_hierarquia', highlighting, formatDocumentHierarchy)}</dd>
                    </div>
                    <div class="col-md-3">
                        <dt>Número Externo</dt>
                        <dd class="color-documento">${returnHighlightedProperty(doc, 'nr_externo', highlighting)}</dd>
                    </div>
                    <div class="col-md-3">
                        <dt>Data do Cadastro</dt>
                        <dd class="color-documento">${formatDate(doc.dt_cadastro)}</dd>
                    </div>
                    <div class="col-md-12">
                        <dt><br>Personagens</dt>
                        <dd class="color-documento">${returnHighlightedProperty(doc, 'ds_info_personagem', highlighting).join('<br>')}</dd>
                    </div>
                </dl>
            </div>
        </div>
    `
}

/**
 * Creates a card for a given ship
 * @param {Object} doc a entity document representing a ship
 * @param {String} doc.ano_construcao Ship build date
 * @param {String} doc.cpf_cnpj Ship owner document
 * @param {String} doc.nome_embarcacao Ship name
 * @param {String} doc.tipo_embarcacao Ship type
 * @param {Object} highlighting highlighted terms returned by search
 * @param {Object} highlighting.uuid a object that has a highlighted term
 * @param {String[]} highlighting.uuid.prop the terms that matches the searched term
 */
const embarcacaoCard = (doc, highlighting) => {
    return `
        <div class="body col-md-12">
            <div class="row">
                <dl>
                    <div class="col-md-4">
                        <dt>CPF/CNPJ do Proprietário</dt>
                        <dd class="color-embarcacao">${returnHighlightedProperty(doc, 'cpf_cnpj', highlighting, formatCPFOrCNPJ)}</dd>
                    </div>
                    <div class="col-md-4">
                        <dt>Tipo da Embarcação</dt>
                        <dd class="color-embarcacao">${doc.tipo_embarcacao}</dd>
                    </div>
                    <div class="col-md-3">
                        <dt>Ano de Construção</dt>
                        <dd class="color-embarcacao">${doc.ano_construcao || '—'}</dd>
                    </div>
                </dl>
            </div>
        </div>
    `
}

/**
 * Creates a card for a given company
 * @param {Object} doc a entity document representing a company
 * @param {String} doc.cnpj Company CNPJ
 * @param {String} doc.cpf_responsavel Company Owner's CPF
 * @param {String} doc.municipio Company City
 * @param {String} doc.razao_social Company Full Name
 * @param {String} doc.responsavel Company Responsible Person
 * @param {String} doc.uf Company UF
 * @param {Object} highlighting highlighted terms returned by search
 * @param {Object} highlighting.uuid a object that has a highlighted term
 * @param {String[]} highlighting.uuid.prop the terms that matches the searched term
 */
const empresaCard = (doc, highlighting) => {
    return `
        <div class="body col-md-12">
            <div class="row">
                <dl>
                    <div class="col-md-3">
                        <dt>CNPJ</dt>
                        <dd class="color-empresa">${returnHighlightedProperty(doc, 'cnpj', highlighting, formatCNPJ)}</dd>
                    </div>
                    <div class="col-md-3">
                        <dt>Nome do Responsável</dt>
                        <dd class="color-empresa">${returnHighlightedProperty(doc, 'responsavel', highlighting)}</dd>
                    </div>
                    <div class="col-md-3">
                        <dt>CPF do Proprietário</dt>
                        <dd class="color-empresa">${returnHighlightedProperty(doc, 'cpf_responsavel', highlighting, formatCPF)}</dd>
                    </div>
                    <div class="col-md-3">
                        <dt>Município / UF</dt>
                        <dd class="color-empresa">${doc.municipio} / ${doc.uf}</dd>
                    </div>
                </dl>
            </div>
        </div>
    `
}
/**
 * 
 * @param {*} rg 
 */
const pessoaFoto = rg => {
    get(`/api/foto?rg=${rg}`, data => {
        if (data.uuid && data.imagem) {
            document.querySelectorAll(`img[data-rg="${rg}"]`).forEach(img => {
                img.setAttribute("src", `data:image/jpeg;base64,${data.imagem}`)
            })
        }
    })
}

/**
 * Creates a card for a given person
 * @param {Object} doc a entity document representing a person
 * @param {String} doc.nome Person's name
 * @param {Number} doc.cpf Person's CPF number, as a Number (so without leading zero)
 * @param {String} doc.nome_mae Person's mother's name
 * @param {String} doc.dt_nasc Person's born date, as a string on the format: YYYY-MM-DD
 * @param {Object} highlighting highlighted terms returned by search
 * @param {Object} highlighting.uuid a object that has a highlighted term
 * @param {String[]} highlighting.uuid.prop the terms that matches the searched term
 */
const pessoaCard = (doc, highlighting) => {
    return `
        <div class="body col-md-12">
            <div class="row">
                <dl>
                    <div class="col-md-3">
                        <dt>CPF</dt>
                        <dd class="color-pessoa">${formatCPF(doc.cpf)}</dd>
                    </div>
                    <div class="col-md-6">
                        <dt>Nome da mãe</dt>
                        <dd class="color-pessoa">${returnHighlightedProperty(doc, 'nome_mae', highlighting)}</dd>
                    </div>
                    <div class="col-md-3">
                        <dt>Data de nascimento</dt>
                        <dd class="color-pessoa">${formatDate(doc.dt_nasc)}</dd>
                    </div>
                </dl>
            </div>
        </div>
    `
}

/**
 * Creates a card for a given vehicle
 * @param {Object} doc a entity document representing a vehicle
 * @param {String} doc.proprietario Vehicle owner's name
 * @param {Number} doc.chassi Vehicle unique chassi number
 * @param {String} doc.renavam Vehicle unique Renavam number
 * @param {String} doc.descricao Vehicle description, with brand, model, year and color
 * @param {Object} highlighting highlighted terms returned by search
 * @param {Object} highlighting.uuid a object that has a highlighted term
 * @param {String[]} highlighting.uuid.prop the terms that matches the searched term
 */
const veiculoCard = (doc, highlighting) => {
    // const caracteristicaVeiculo = `${doc.marca_modelo.trim()} ${doc.ano_modelo} ${doc.cor.trim()}`
    // get(`/api/foto-veiculo?caracteristicas=${caracteristicaVeiculo}`, addVeiculoFoto)
    // <img data-caracteristica="${caracteristicaVeiculo}" src="/static/img/icon/veiculo.svg" />
    return `
        <dl>
            <div class="col-md-3">
                <dt>Chassis</dt>
                <dd class="color-veiculo">${returnHighlightedProperty(doc, 'chassi', highlighting)}</dd>
            </div>
            <div class="col-md-2">
                <dt>Renavam</dt>
                <dd class="color-veiculo">${returnHighlightedProperty(doc, 'renavam', highlighting)}</dd>
            </div>
            <div class="col-md-7">
                <dt>Proprietário</dt>
                <dd class="color-veiculo">${returnHighlightedProperty(doc, 'proprietario', highlighting)}</dd>
            </div>
        </dl>
    `
}

/**
 * Returns a matching highlighting property value from the document, or the value itself
 * @param {Object} doc 
 * @param {String} doc.uuid
 * @param {String} doc[prop]
 * @param {String} prop 
 * @param {Object} highlighting 
 * @param {Object} highlighting[uuid]
 * @param {String[]} highlighting[uuid][prop]
 * @param {Function} formatFn Applies a formatting function, if available
 */
const returnHighlightedProperty = (doc, prop, highlighting, formatFn) => {
    if (highlighting[doc.uuid] && highlighting[doc.uuid][prop]) {
        if (formatFn) {
            return `<em>${formatFn(highlighting[doc.uuid][prop][0].replace(/<\/?em>/g, ''))}</em>`
        }
        if (prop === 'ds_info_personagem') {
            let filteredElem = highlighting[doc.uuid][prop][0]
            let filteredElemNoHighlight = filteredElem.replace(/<\/?em>/g, '')
            let filteredArray = doc[prop].filter(e => e !== filteredElemNoHighlight)
            return [].concat(filteredElem).concat(filteredArray)
        }
        return highlighting[doc.uuid][prop][0]
    }
    if (doc[prop]) {
        if (formatFn) {
            return formatFn(doc[prop])
        }
        return doc[prop]
    }
    return 'desconhecido'
}