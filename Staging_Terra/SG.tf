# SEC GROUP
resource "aws_security_group" "web_ssh" {
  name        = "ssh-access"
  description = "open ssh traffic"
  vpc_id      = aws_vpc.finance-vpc.id
 
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
 
  }
  
  ingress {
    from_port = 8000
    to_port = 8000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
 
  tags = {
    "Name" : "TerraSG"
    "Terraform" : "true"
  }
 
}


resource "aws_security_group" "database_sg" {
    name = "Database security group"
    description = "MySQL database access"
    vpc_id = aws_vpc.finance-vpc.id

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 3306
        to_port = 3306
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
  }
  
    tags = {
        "Name" : "DBSG"
        "Terraform" : "true"
  }

}
