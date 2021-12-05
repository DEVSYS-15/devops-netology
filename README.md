#Содержание
## 1. gitignor


# gitignor
## Исключена локальная директория 
**/.terraform/*

## файлы по следующим маскам
*.tfstate
*.tfstate.*

## лог падений
crash.log

## файлы ключей и настроек переменного окружения 
*.tfvars

## временные файлы
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# Include override files you do wish to add to version control using negated pattern
#
# !example_override.tf

# Include tfplan files to ignore the plan output of command: terraform plan -out=tfplan
# example: *tfplan*

# файлы настроек CLI
.terraformrc
terraform.rc



