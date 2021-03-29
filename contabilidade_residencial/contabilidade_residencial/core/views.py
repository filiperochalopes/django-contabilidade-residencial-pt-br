from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from .models import Pessoa, PropriedadePessoa, Banco, Registro, Tag


def registros(request):
    registros = Registro.objects.all()
    return render(request, 'registros.html', {'registros': registros})


def adicionar_registro(request):
    mensagem = None
    cor = None
    pessoas = Pessoa.objects.all()
    if request.method == 'POST':
        try:
            registro = Registro()
            pessoa = Pessoa.objects.get(id=request.POST.get('pessoa_id'))
            banco = Banco.objects.get(id=request.POST.get('banco_id'))
            registro.pessoa = pessoa
            registro.banco = banco
            registro.valor = request.POST.get('valor')
            registro.descricao = request.POST.get('descricao')
            tags = request.POST.getlist('tags[]')
            registro.save()

            for tag in tags:
                if tag.nome is not None and tag.nome != '':
                    try:
                        novaTag = Tag()
                        novaTag.nome = tag
                        novaTag.cor_hex = 'cccccc'
                        novaTag.save()
                        registro.tags.add(novaTag)
                    except:
                        try:
                            tagExistente = Tag.objects.get(nome=tag)
                            registro.tags.add(tagExistente)
                        except Exception as e:
                            raise(e)
                            mensagem = f"Erro ao adicionar: {e}"
                            cor = "#e52222"

            mensagem = "Adicionado com sucesso!"
            cor = "#7ee534"
        except Exception as e:
            mensagem = f"Erro ao adicionar: {e}"
            cor = "#e52222"

    return render(request, 'adicionar_registro.html', {'mensagem': mensagem, 'cor': cor, 'pessoas': pessoas})


def editar_registro(request):
    return render(request, 'editar_registro.html')


def pessoas(request):
    mensagem = None
    cor = None
    if(request.GET.get('delete')):
        delete_id = request.GET.get('delete')
        try:
            pessoa = Pessoa.objects.get(id=delete_id)
            pessoa.delete()
            mensagem = f'{pessoa.nome} excluído(a) com sucesso'
            cor = "#7ee534"
        except Pessoa.DoesNotExist:
            mensagem = f'Pessoa de id {delete_id} não existe'
            cor = '#e52222'
    pessoas = Pessoa.objects.all()
    for pessoa in pessoas:
        propriedades = PropriedadePessoa.objects.filter(pessoa=pessoa)
        pessoa.propriedades = propriedades
        bancos = Banco.objects.filter(pessoa=pessoa)
        pessoa.bancos = bancos
    return render(request, 'pessoas.html', {'pessoas': pessoas, 'mensagem': mensagem, 'cor': cor})


def adicionar_pessoa(request):
    mensagem = None
    cor = None
    if request.method == 'POST':
        pessoa = Pessoa()
        pessoa.nome = request.POST.get('nome')
        pessoa.email = request.POST.get('email')
        pessoa.save()
        propriedades = [[request.POST.getlist('propriedades_chave[]')[i], request.POST.getlist('propriedades_valor[]')[
            i]] for i in range(len(request.POST.getlist('propriedades_chave[]')))]

        for propriedade in propriedades:
            propriedade_pessoa = PropriedadePessoa()
            propriedade_pessoa.chave = propriedade[0]
            propriedade_pessoa.valor = propriedade[1]
            propriedade_pessoa.pessoa = pessoa
            propriedade_pessoa.save()

        mensagem = "Adicionado com sucesso!"
        cor = "#7ee534"

    return render(request, 'adicionar_pessoa.html', {'mensagem': mensagem, 'cor': cor})


def editar_pessoa(request):
    pessoa = Pessoa.objects.get(id=request.GET.get('id'))
    propriedades = PropriedadePessoa.objects.filter(pessoa=pessoa)
    pessoa.propriedades = propriedades

    return render(request, 'editar_pessoa.html', {'pessoa': pessoa})


def bancos(request):
    return render(request, 'bancos.html')


def adicionar_banco(request):
    mensagem = None
    cor = None
    pessoas = Pessoa.objects.all()
    if request.method == 'POST':
        pessoa = Pessoa.objects.get(id=request.POST.get('pessoa_id'))
        banco = Banco()
        banco.pessoa = pessoa
        banco.apelido = request.POST.get('apelido')
        banco.codigo = request.POST.get('codigo')
        banco.nome = request.POST.get('nome')
        banco.agencia = request.POST.get('agencia')
        banco.conta = request.POST.get('conta')
        try:
            banco.save()
            mensagem = "Adicionado com sucesso!"
            cor = "#7ee534"
        except Exception as e:
            mensagem = f"Erro ao adicionar {e}"
            cor = "#e52222"

    return render(request, 'adicionar_banco.html', {'mensagem': mensagem, 'cor': cor, 'pessoas': pessoas})


def editar_banco(request):
    return render(request, 'editar_banco.html')


def tags(request):
    tags = Tag.objects.all()
    return render(request, 'tags.html', {'tags': tags})


def rest_banco(request):
    pessoa = Pessoa.objects.get(id=request.GET.get('pessoa_id'))
    bancos = Banco.objects.filter(pessoa=pessoa)
    serialized_query = serializers.serialize('json', bancos)
    return JsonResponse(serialized_query, safe=False)