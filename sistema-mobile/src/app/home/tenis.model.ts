export class Tenis
{
    public id: number;
    public marca: number;
    public nome_marca: string;
    public modelo: string;
    public tamanho: number;
    public cor: number;
    public nome_cor: string;
    public foto: string | undefined;
    public tipo: number;
    public nome_tipo: string;

    constructor() {
        this.id = 0;
        this.marca = 0;
        this.nome_marca = '';
        this.modelo = '';
        this.tamanho = 0;
        this.cor = 0;
        this.nome_cor = '';
        this.tipo = 0;
        this.nome_tipo = '';
    }
}