import {
    formatCPF,
    formatDate,
    get,
} from '/static/js/utils.js'

/**
 * Creates a card for a doc/entity
 * @param {Object} entity data for this entity
 * @param {String} key the entity type (empresa, pessoa, veiculo)
 * @param {*} data The whole data returned from API, to get highlight information
 * @param {bool} isExtended whether the card is being called within the search list result or in the searchDetails screen
 * @param {bool} bondSearchId wheter the card is a result of the bond search
*/
export const entityCard = (entity, key, data, isExtended, bondSearchId) => {
    let onclickFn = `onclick="searchDetailStep('${entity.uuid}', '${key}')"`
    if (isExtended) {
        onclickFn = ''
    }
    if (bondSearchId) {
        onclickFn = `onclick="doBondSearch(${bondSearchId}, ${entity.uuid})"`
    }
    let ret = `<div class="card-resultado clearfix" ${onclickFn}>`
    switch(key) {
        case 'pessoa':
            ret += pessoaCard(entity, data, isExtended)
            break
        case 'veiculo':
            ret += veiculoCard(entity, data, isExtended)
            break
        default:
            // just spit it out
            ret += JSON.stringify(entity)
    }
    ret += `</div>`
    return ret
}

/**
 * Creates a card for a given person
 * @param {Object} doc a entity document representing a person
 * @param {String} doc.nome Person's name
 * @param {Number} doc.num_cpf Person's CPF number, as a Number (so without leading zero)
 * @param {String} doc.nome_mae Person's mother's name
 * @param {String} doc.data_nascimento Person's born date, as a string on the format: YYYY-MM-DD
 * @param {Object} data data from API
 * @param {Object} data.pessoa 
 * @param {Object} data.pessoa.highlighting highlighted terms returned by search
 * @param {Object} data.pessoa.highlighting.uuid a object that has a highlighted term
 * @param {String[]} data.pessoa.highlighting.uuid.prop the terms that matches the searched term
 * @param {bool} isExtended whether the card is being called within the search list result or in the searchDetails screen
 */
const pessoaCard = (doc, data, isExtended) => {
    let titleClass = 'col-lg-2 text-center'
    let bodyClass = 'col-lg-10'
    let backFn = ''
    if (isExtended) {
        titleClass = 'col-lg-12 text-center title'
        bodyClass = 'col-lg-12'
        backFn = 'onclick="backToSearch()"'
    }
    return `
        <div class="${titleClass}">
            <img src="/static/img/icon/pessoa.svg" />
        </div>
        <div class="${bodyClass}">
            <div class="row">
                <div class="col-lg-12">
                    <h3 class="color-pessoa" ${backFn}>${returnHighlightedProperty(doc, 'nome', data.pessoa.highlighting)}</h3>
                </div>
                <div class="body col-lg-12">
                    <div class="row">
                        <dl>
                            <div class="col-lg-3">
                                <dt>CPF</dt>
                                <dd class="color-pessoa">${formatCPF(doc.num_cpf)}</dd>
                            </div>
                            <div class="col-lg-6">
                                <dt>Nome da mãe</dt>
                                <dd class="color-pessoa">${returnHighlightedProperty(doc, 'nome_mae', data.pessoa.highlighting)}</dd>
                            </div>
                            <div class="col-lg-3">
                                <dt>Data de nascimento</dt>
                                <dd class="color-pessoa">${formatDate(doc.data_nascimento)}</dd>
                            </div>
                        </dl>
                    </div>
                </div>
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
 * @param {Object} data data from API
 * @param {Object} data.veiculo 
 * @param {Object} data.veiculo.highlighting highlighted terms returned by search
 * @param {Object} data.veiculo.highlighting.uuid a object that has a highlighted term
 * @param {String[]} data.veiculo.highlighting.uuid.prop the terms that matches the searched term
 * @param {bool} isExtended whether the card is being called within the search list result or in the searchDetails screen
 */
const veiculoCard = (doc, data, isExtended) => {
    let titleClass = 'col-lg-2 text-center'
    let bodyClass = 'col-lg-10'
    let backFn = ''
    if (isExtended) {
        titleClass = 'col-lg-12 text-center title'
        bodyClass = 'col-lg-12'
        backFn = 'onclick="backToSearch()"'
    }
    const caracteristicaVeiculo = `${doc.marca} ${doc.modelo} ${doc.cor}`

    get(`/api/foto-veiculo?caracteristicas=${caracteristicaVeiculo}`, addVeiculoFoto)
    return `
        <div class="${titleClass}">
            <img data-caracteristica="${caracteristicaVeiculo}" src="/static/img/icon/veiculo.svg" />
        </div>
        <div class="${bodyClass}">
            <div class="row">
                <div class="col-lg-12">
                    <h3 class="color-veiculo" ${backFn}>${returnHighlightedProperty(doc, 'descricao', data.veiculo.highlighting)}</h3>
                </div>
                <dl>
                    <div class="col-lg-3">
                        <dt>Chassis</dt>
                        <dd class="color-veiculo">${returnHighlightedProperty(doc, 'chassi', data.veiculo.highlighting)}</dd>
                    </div>
                    <div class="col-lg-2">
                        <dt>Renavam</dt>
                        <dd class="color-veiculo">${returnHighlightedProperty(doc, 'renavam', data.veiculo.highlighting)}</dd>
                    </div>
                    <div class="col-lg-7">
                        <dt>Proprietário</dt>
                        <dd class="color-veiculo">${returnHighlightedProperty(doc, 'proprietario', data.veiculo.highlighting)}</dd>
                    </div>
                </dl>
            </div>
        </div>
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
 */
const returnHighlightedProperty = (doc, prop, highlighting) => {
    if (highlighting[doc.uuid] && highlighting[doc.uuid][prop]) {
        return highlighting[doc.uuid][prop][0]
    }
    if (doc[prop]) {
        return doc[prop]
    }
    return 'desconhecido'
}