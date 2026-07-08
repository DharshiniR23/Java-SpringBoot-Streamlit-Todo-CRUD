package com.example.demo;



import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TodoApplication {
    public static void main(String[] args) {
        SpringApplication.run(TodoApplication.class, args);
        System.out.println("==================================");
        System.out.println("✅ Todo API is running!");
        System.out.println("📋 API URL: http://localhost:8087/api/todos");
        System.out.println("==================================");
    }
}