<!--
Sync Impact Report
Version change: 0.0.0 -> 1.0.0
Modified principles: none -> Simplicidade; Qualidade de Código; Segurança; Testes; Integração, Entrega e Infraestrutura
Added sections: Requisitos de Infraestrutura e Containerização; Fluxo de Desenvolvimento e Governança
Removed sections: none
Deferred items: none
-->

# Atividade SDD Constitution

## Core Principles

### I. Simplicidade
A solução deve implementar apenas o que é estritamente necessário para atender aos requisitos da atividade. Funcionalidades, dependências, frameworks e padrões complexos só devem ser adotados quando houver justificativa técnica clara e mensurável. A simplicidade é obrigatória como princípio de desenho e manutenção.

### II. Qualidade de Código
O código deve ser organizado, legível e fácil de manter. Nomes de funções, classes, variáveis e arquivos devem ser claros e expressivos. A separação de responsabilidades entre interface, regras de negócio e persistência é obrigatória para reduzir acoplamento e facilitar evoluções futuras.

### III. Segurança
Todas as entradas recebidas pela aplicação devem ser validadas antes de qualquer processamento. Nenhuma credencial, senha, token, chave ou dado sensível pode ser armazenado diretamente no código-fonte. Configurações secretas devem ser fornecidas por variáveis de ambiente, arquivos de secrets ou mecanismos equivalentes. O pipeline de entrega deve executar análise de segurança antes do deploy, e o deploy só poderá ocorrer após a conclusão bem-sucedida das etapas anteriores.

### IV. Testes
As principais funcionalidades da aplicação devem possuir testes automatizados e repetíveis. A execução de testes deve acontecer automaticamente no pipeline antes do deploy. Correções de regressão devem ser validadas com evidência do problema resolvido e da ausência de retorno do defeito.

### V. Integração, Entrega Contínua e Infraestrutura
O projeto deve ser versionado no GitHub, usando a branch main como referência da versão de produção. Alterações enviadas para main devem disparar automaticamente a pipeline de validação, testes, análise de segurança e deploy. A aplicação deve ser executável via Docker, utilizar o mesmo ambiente localmente e em AWS, ficar acessível publicamente pela internet em uma instância EC2 e seguir uma estratégia de entrega contínua documentada.

## Requisitos de Infraestrutura e Containerização

A aplicação deve ser empacotada para execução em Docker, garantindo que o mesmo ambiente seja reutilizável em desenvolvimento e produção. A infraestrutura deve ser provisionada em uma instância EC2 da AWS, e a aplicação deve permanecer acessível publicamente pela internet após o deploy. Os requisitos de infraestrutura devem ser documentados de forma clara para permitir reprodução, manutenção e operação segura do ambiente.

## Documentação e Operação

O README deve explicar o objetivo do projeto, as tecnologias utilizadas, a execução local, a pipeline CI/CD, o scanner de segurança e a arquitetura de deploy. A documentação deve ser mantida atualizada conforme mudanças relevantes no projeto para permitir entendimento rápido do sistema, configuração do ambiente e processos de operação.

## Governance

Esta Constituição define as regras mínimas de desenvolvimento, segurança, qualidade e entrega do projeto. Qualquer alteração nesta documentação deve incluir justificativa, revisão explícita do impacto e indicação da nova versão. Mudanças em princípios ou regras operacionais só entram em vigor após análise e aprovação do responsável pelo projeto. A conformidade com a Constituição deve ser verificada por evidências, incluindo testes, validações de segurança, documentação correta e rastreabilidade do processo de entrega.

**Version**: 1.0.0 | **Ratified**: 2026-09-22 | **Last Amended**: 2026-09-22
