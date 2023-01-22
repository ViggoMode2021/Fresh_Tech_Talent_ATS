terraform {
  cloud {
    organization = "TerraformVig"

    workspaces {
      name = "provisioners"
    }
  }
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

data "template_file" "user_data" {
  template = file("./userdata.yml")
}

resource "aws_instance" "amazon-linux-2-with-nginx-and-flask-application" {
  ami                         = var.ami
  instance_type               = var.instance-type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [var.vpc_security_group_ids]
  associate_public_ip_address = true
  user_data                   = data.template_file.user_data.rendered

  tags = {
    Name = "Amazon Linux 2 with Nginx server and Flask app running on port 8080"
  }
}

output "instance_ip_addr" {
  value = join("", [aws_instance.amazon-linux-2-with-nginx-and-flask-application.public_ip, ":8080"])
}
