const DOMINIO = 'http://apps.mprj.mp.br/sistema/dominio'

export const addStyleToNode = node => {
    let color = '#7bb3ff'

    switch (getNodeType(node)) {
        case 'empresa':
            color = '#51c881'
            break
        case 'mgp':
            color = '#ab897f'
            break
        case 'multa':
            color = '#ff524e'
            break
        case 'orgao':
            color = '#ffb842'
            break
        case 'personagem':
            color = '#a176d1'
            break
        case 'pessoa':
            color = '#00d1e2'
            break
        case 'telefone':
            color = '#324eb6'
            break
        case 'veiculo':
            color = '#ff8b63'
            break
    }

    return {
        ...node,
        color,
        shape: 'circularImage',
        image: `/static/img/icon/${getNodeType(node)}.svg`,
    }
}

/**
 * Format a given key according to a given property
 * @param {String} prop property to format
 * @param {String} key key to format
 */
export const formatKeyString = (prop, key) => {
    switch (prop) {
        case 'cldc_ds_hierarquia':
            return formatDocumentHierarchy(key)
        case 'cnae':
            return formatCNAE(key)
        case 'cnpj':
            return formatCNPJ(key)
        case 'cpf':
        case 'cpf_responsavel':
        case 'num_cpf':
            return formatCPF(key)
        case 'cpfcnpj':
        case 'cpfcgc':
        case 'cpf_cnpj':
            return formatCPFOrCNPJ(key)
        case 'data':
        case 'data_inicio':
        case 'data_nascimento':
        case 'datainfra':
        case 'dt_cadastro':
        case 'dt_criacao':
        case 'dt_extincao':
        case 'dt_nasc':
        case 'pers_dt_inicio':
        case 'pers_dt_fim':
            return formatDate(key)
        case 'ident':
            return formatCPFOrCNPJ(key)
        case 'nr_externo':
            return formatExternalNumberLink(key)
        case 'nr_mp':
            return formatMPRJLink(key)
        case 'placa':
            return formatVehiclePlate(key)
        case 'rg':
        case 'num_rg':
            return formatRG(key)
        case 'ind_sexo':
            return formatGender(key)
        default:
            return key
    }
}

/**
 * Adds diacritics (a => á) and formats props case.
 *
 * @param {string} text The prop string to be formatted.
 */
export const formatPropString = text => {
    switch (text) {
        // 1st Level
        case 'veiculo':
            return 'Veículo'
        case 'orgao':
            return 'Órgão'
        case 'mgp':
            return 'MGP'
        // Documento
        case 'cldc_ds_hierarquia':
            return 'Hierarquia de Classe do Documento'
        case 'nr_externo':
            return 'Número Externo'
        case 'nr_mp':
            return 'Número MPRJ'
        // Embarcação
        case 'ano_construcao':
            return 'Ano de Construção'
        case 'cpf_cnpj':
            return 'CPF / CNPJ do Proprietário'
        case 'nome_embarcacao':
            return 'Nome da Embarcação'
        case 'nr_inscricao':
            return 'Número de Inscrição'
        case 'tipo_embarcacao':
            return 'Tipo da Embarcação'
        // Empresa
        case 'cnae':
            return 'CNAE'
        case 'cnpj':
            return 'CNPJ'
        case 'cpf_responsavel':
            return 'CPF do Responsável'
        case 'data_inicio':
            return 'Data de Início'
        case 'municipio':
            return 'Município'
        case 'nome_responsavel':
            return 'Nome do Responsável'
        case 'razao_social':
            return 'Razão Social'
        case 'uf':
            return 'UF'
        // MGP
        case 'cdorgao':
            return 'Código do Órgão'
        case 'docu_dk':
            return 'ID do Documento'
        case 'dt_cadastro':
            return 'Data do Cadastro'
        case 'nr_ext':
            return 'Número Externo'
        case 'nr_mprj':
            return 'Número MPRJ'
        // Multa
        case 'autoinfra':
            return 'Número do Auto de Infração'
        case 'datainfra':
            return 'Data'
        case 'desc':
        case 'descinfra':
            return 'Descrição'
        case 'proprietario':
            return 'Proprietário'
        // Órgão
        case 'craai':
            return 'CRAAI'
        case 'dt_criacao':
            return 'Data de Criação'
        case 'dt_extincao':
            return 'Data de Extinção'
        case 'nm_comarca':
            return 'Comarca'
        case 'nm_foro':
            return 'Foro'
        case 'nm_orgao':
            return 'Órgão'
        case 'nm_regiao':
            return 'Região'
        case 'nm_tporgao':
            return 'Tipo do Órgão'
        case 'sensivel':
            return 'Sensível'
        case 'situacao':
            return 'Situação'
        // Pessoa
        case 'ind_sexo':
            return 'Sexo'
        case 'num_cpf':
            return 'CPF'
        case 'dt_nasc':
            return 'Data de Nascimento'
        case 'nome_mae':
            return 'Nome da Mãe'
        case 'nome_pai':
            return 'Nome do Pai'
        case 'nome_rg':
            return 'Nome no RG'
        case 'num_rg':
            return 'RG'
        case 'sigla_uf':
            return 'UF'
        // Personagem
        case 'cpfcnpj':
            return 'CPF/CNPJ'
        case 'pers_dt_inicio':
            return 'Data de Início'
        case 'pers_dt_fim':
            return 'Data de Fim'
        case 'pess_nm_pessoa':
            return 'Nome da Pessoa'
        case 'tppe_descricao':
            return 'Descrição'
        // Telefone
        case 'numero':
            return 'Número'
        // Veículo
        case 'cpfcgc':
            return 'CPF/CNPJ'
        case 'descricao_cor':
            return 'Cor'
        case 'fabric':
            return 'Ano Fabricação'
        case 'modelo':
            return 'Ano Modelo'
        default:
            return text.split('_').map(word => word.substr(0, 1).toUpperCase() + word.substr(1)).join(' ')
    }
}

export const formatAddresses = addresses => {
    if (addresses.length === 0) {
        return `Não há endereço cadastrado para esta pessoa.`
    }
    return addresses.map(address => formatAddress(address)).join('')
}

const formatAddress = address => {
    return `<dl class="address">
        <dt>Rua:</dt>
        <dd>${address.endereco}</dd>
        <dt>Número:</dt>
        <dd>${address.numero}</dd>
        <dt>Complemento:</dt>
        <dd>${address.complemento}</dd>
        <dt>Bairro:</dt>
        <dd>${address.bairro}</dd>
        <dt>Cidade:</dt>
        <dd>${address.cidade}</dd>
        <dt>UF:</dt>
        <dd>${address.sigla_uf}</dd>
        <dt>Telefone:</dt>
        <dd>${address.telefone}</dd>
    </dl>`
}

/**
 * Format as CNAE - xxxx-x/xx
 * @param {String} cnae
 */
export const formatCNAE = cnae => {
    return `${cnae.substr(0,4)}-${cnae.substr(4,1)}/${cnae.substr(5)}`
}

/**
 * Formats as CNPJ - xx.xxx.xxx/xxxx-xx
 * @param {String} cnpj
 */
export const formatCNPJ = cnpj => {
    if (cnpj.length === 14) {
        return `${cnpj.substr(0,2)}.${cnpj.substr(2,3)}.${cnpj.substr(5,3)}/${cnpj.substr(8,4)}-${cnpj.substr(12)}`
    }
    return cnpj
}

/**
 * Formats as CPF - xxx.xxx.xxx-xx
 * @param {String} cpf
 */
export const formatCPF = cpf => {
    cpf = cpf.toString().padStart(11, "0")
    if (cpf.length === 11) {
        return `${cpf.substr(0,3)}.${cpf.substr(3,3)}.${cpf.substr(6,3)}-${cpf.substr(9)}`
    }
    return cpf
}

/**
 * Formats as Date - from yyyymmdd to dd/mm/yyyy
 * @param {String} date
 */
export const formatDate = date => {
    if (date.length === 8) {
        return `${date.substr(6,2)}/${date.substr(4,2)}/${date.substr(0,4)}`
    }
    return `${date.substr(8,2)}/${date.substr(5,2)}/${date.substr(0,4)}`
}

/**
 * Format Document Hierarchy Class List
 * @param {*} str
 */
export const formatDocumentHierarchy = str => {
    let strArray = str.split('|')
    strArray[0] = strArray[0].split(' ').map(word => word.substr(0, 1).toUpperCase() + word.substr(1).toLowerCase()).join(' ')
    return strArray.join(' > ')
}

/**
 * Returns a Link to Domínio searching for a external number.
 * @param {String} num
 */
export const formatExternalNumberLink = num => `<a href="${DOMINIO}/#/document-search/${num}" target="_blank">${num}</a>`

/**
 * Formats Gender string
 * @param {String} genderId
 */
export const formatGender = genderId => {
    switch (genderId) {
        case "M":
            return "Masculino"
        case "F":
            return "Feminino"
        default:
            return genderId
    }
}

/**
 * Formats number as MPRJ Document number
 * @param {String} num
 */
export const formatMPRJ = num => `${num.substr(0,4)}.${num.substr(4)}`

/**
 * Returns a Link to Domínio searching for a MPRJ number
 * @param {String} num
 */
export const formatMPRJLink = num => `<a href="${DOMINIO}/#/document-search/${num}" target="_blank">${formatMPRJ(num)}</a>`

/**
 * Format RG on Detran format - xx.xxx.xxx-x
 * @param {String} rg
 */
export const formatRG = rg => {
    if (rg.length === 9) {
        return `${rg.substr(0,2)}.${rg.substr(2,3)}.${rg.substr(5,3)}-${rg.substr(-1)}`
    }
    return rg
}

/**
 * Format Vehicle Ident as CPF or CNPJ
 * @param {String} ident Vehicle owner ident
 */
export const formatCPFOrCNPJ = ident => {
    // ident is the PK of vehicle owner, either CPF or CNPJ
    // we will naively assume that if it starts with three zeroes, its a CPF, otherwise, it should be a CNPJ
    if (ident.length === 11) {
        return formatCPF(ident)
    }
    if (ident.substr(0,3) === '000') {
        return formatCPF(ident.substr(3))
    }
    formatCNPJ(ident)
}

/**
 * Format as Vehicle Plate - XXX-XXXX
 * @param {string} plate
 * @return {string}
 */
export const formatVehiclePlate = plate => {
    if (plate.length === 7) {
        return `${plate.substr(0,3)}-${plate.substr(3)}`
    }
    return plate
}

/**
 * Make a HTTP GET call and returns the data.
 *
 * @param {String} url The URL to GET.
 * @param {Function} callback A function to be executed with the returned data.
 */
export const get = (url, callback) => {
    var xmlhttp = new XMLHttpRequest()
    xmlhttp.open('GET', url, true)
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4) {
            if (xmlhttp.status == 200) {
                var obj = JSON.parse(xmlhttp.responseText)
                if (callback) {
                    callback(obj)
                }
            } else {
                alert('Erro ao carregar os dados.')
            }
        }
    }
    xmlhttp.send(null)
}

/**
 * Returns a node type.
 *
 * @param {*} node 
 */
export const getNodeType = node => {
    return node.type[0].toLowerCase()
}

/**
 * Sanitizes a string to use on search API - removes diacritics (á, ç etc.) and makes it uppercase
 * @param {String} string A string to be sanitized
 */
export const sanitizeQuery = string => {
    if (string.normalize) {
        return string.normalize('NFD').replace(/[\u0300-\u036f]/g, "").toUpperCase()
    }
    return string.toUpperCase()
}

/**
 * Formats number with thousands separators - NNNNN => NN.NNN
 * @param {string|number} num number to be formatted
 * @returns {string}
 */
export const thousandsSeparator = num => {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.')
}

export const showLoading = () => {
    document.getElementById('loading').className = ''
}

export const hideLoading = () => {
    document.getElementById('loading').className = 'hidden'
}

export const getCardTitle = (nodeType) => {
    switch (nodeType) {
        case 'pessoa':
            return 'nome'
        case 'veiculo':
            return 'descricao'
        default:
            return null
    }
}