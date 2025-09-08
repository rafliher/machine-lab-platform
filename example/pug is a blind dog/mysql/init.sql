-- MySQL dump 10.13  Distrib 8.4.5, for Linux (x86_64)
--
-- Host: localhost    Database: db_landing
-- ------------------------------------------------------
-- Server version	8.4.5

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `pages`
--

DROP TABLE IF EXISTS `pages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pages`
--

LOCK TABLES `pages` WRITE;
/*!40000 ALTER TABLE `pages` DISABLE KEYS */;
INSERT INTO `pages` VALUES (1,'about','doctype html\r\nhtml(lang=\"en\")\r\n  head\r\n    meta(charset=\"UTF-8\")\r\n    meta(name=\"viewport\" content=\"width=device-width, initial-scale=1.0\")\r\n    title About Us - Amazing Company\r\n    link(rel=\"stylesheet\", href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\")\r\n    link(rel=\"stylesheet\", href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css\")\r\n    style.\r\n      body {\r\n        font-family: Arial, sans-serif;\r\n      }\r\n      .hero {\r\n        background: linear-gradient(135deg, #007bff, #00c6ff);\r\n        color: white;\r\n        text-align: center;\r\n        padding: 80px 20px;\r\n      }\r\n      .section-light {\r\n        background-color: #f8f9fa;\r\n      }\r\n      .section-dark {\r\n        background-color: #343a40;\r\n        color: white;\r\n      }\r\n      .team-photo {\r\n        width: 100%;\r\n        height: auto;\r\n        border-radius: 12px;\r\n      }\r\n\r\n  body\r\n    // Navbar\r\n    nav.navbar.navbar-expand-lg.navbar-dark.bg-dark\r\n      .container\r\n        a.navbar-brand(href=\"/\") Amazing Company\r\n        button.navbar-toggler(type=\"button\" data-bs-toggle=\"collapse\" data-bs-target=\"#navbarNav\")\r\n          span.navbar-toggler-icon\r\n        #navbarNav.collapse.navbar-collapse\r\n          ul.navbar-nav.ms-auto\r\n            li.nav-item\r\n              a.nav-link(href=\"/\") Home\r\n            li.nav-item\r\n              a.nav-link.active(href=\"/?page=about\") About Us\r\n\r\n    // Hero Section\r\n    section.hero\r\n      .container\r\n        h1 About Amazing Company\r\n        p Building the future through innovation, dedication, and integrity.\r\n\r\n    // Company History\r\n    section.container.py-5\r\n      .row.align-items-center\r\n        .col-md-6\r\n          h2 Our Journey\r\n          p Founded in 2015, Amazing Company began with a simple mission ΓÇö to deliver impactful technology that transforms businesses. From a small startup to a global consultancy, our journey has been driven by a relentless pursuit of excellence.\r\n        .col-md-6\r\n          img.img-fluid(src=\"https://via.placeholder.com/600x400\" alt=\"Company History\")\r\n\r\n    // Mission and Vision\r\n    section.section-light.py-5\r\n      .container\r\n        .row\r\n          .col-md-6\r\n            h3 Our Mission\r\n            p We aim to empower organizations through smart, scalable, and secure technology solutions that drive growth and resilience.\r\n          .col-md-6\r\n            h3 Our Vision\r\n            p To be the most trusted technology partner for companies looking to innovate, scale, and lead in their industries.\r\n\r\n    // Core Values\r\n    section.container.py-5\r\n      h2.text-center.mb-4 Our Core Values\r\n      .row.text-center\r\n        each value in [{icon: \"lightbulb\", title: \"Innovation\"}, {icon: \"hands-helping\", title: \"Collaboration\"}, {icon: \"shield-alt\", title: \"Integrity\"}, {icon: \"medal\", title: \"Excellence\"}]\r\n          .col-md-3.mb-4\r\n            i.fas(class=`fa-${value.icon} service-icon`)\r\n            h5.mt-2= value.title\r\n\r\n    // Team Section\r\n    - var team = [{name:\"Alice Chen\",title:\"CEO\",img:\"https://i.pravatar.cc/300?u=1\"}, {name:\"Mark Thompson\",title:\"CTO\",img:\"https://i.pravatar.cc/300?u=2\"}, {name:\"Sofia Reyes\",title:\"Head of Design\",img:\"https://i.pravatar.cc/300?u=3\"}, {name:\"Liam Patel\",title:\"Lead Engineer\",img:\"https://i.pravatar.cc/300?u=4\"}]\r\n    section.section-light.py-5\r\n      .container\r\n        h2.text-center.mb-4 Meet Our Team\r\n        .row\r\n          each member in team\r\n            .col-md-3.text-center\r\n              img.team-photo.mb-3(src=member.img alt=member.name)\r\n              h5= member.name\r\n              p.text-muted= member.title\r\n\r\n\r\n    // Call to Action\r\n    section.section-dark.text-center.py-5\r\n      .container\r\n        h2 Want to Work With Us?\r\n        p LetΓÇÖs collaborate to create something exceptional.\r\n        a.btn.btn-outline-light.btn-lg(href=\"/#contact\") Get in Touch\r\n\r\n    // Footer\r\n    footer.text-center.py-4.bg-dark.text-light\r\n      p &copy; 2025 Amazing Company. All rights reserved.\r\n'),(2,'dashboard','doctype html\r\nhtml(lang=\"en\")\r\n  head\r\n    meta(charset=\"UTF-8\")\r\n    meta(name=\"viewport\" content=\"width=device-width, initial-scale=1.0\")\r\n    title Amazing Company - Innovating the Future\r\n    link(rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\")\r\n    link(rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css\")\r\n    style.\r\n      body {\r\n        font-family: Arial, sans-serif;\r\n      }\r\n      .hero {\r\n        background: linear-gradient(135deg, #007bff, #00c6ff);\r\n        color: white;\r\n        text-align: center;\r\n        padding: 100px 20px;\r\n      }\r\n      .service-icon {\r\n        font-size: 40px;\r\n        color: #007bff;\r\n      }\r\n      .section-light {\r\n        background-color: #f8f9fa;\r\n      }\r\n      .section-dark {\r\n        background-color: #343a40;\r\n        color: white;\r\n      }\r\n\r\n  body\r\n    // Navbar\r\n    nav.navbar.navbar-expand-lg.navbar-dark.bg-dark\r\n      .container\r\n        a.navbar-brand(href=\"/\") Amazing Company\r\n        button.navbar-toggler(type=\"button\" data-bs-toggle=\"collapse\" data-bs-target=\"#navbarNav\")\r\n          span.navbar-toggler-icon\r\n        #navbarNav.collapse.navbar-collapse\r\n          ul.navbar-nav.ms-auto\r\n            li.nav-item\r\n              a.nav-link(href=\"/\") Home\r\n            li.nav-item\r\n              a.nav-link(href=\"/?page=about\") About Us\r\n\r\n    // Hero Section\r\n    section.hero\r\n      .container\r\n        h1 Welcome to Amazing Company\r\n        p Leading innovation and technology to empower businesses.\r\n        a.btn.btn-light.btn-lg(href=\"#services\") Explore Our Services\r\n\r\n    // Services Section\r\n    section#services.container.py-5\r\n      h2.text-center.mb-4 Our Services\r\n      .row\r\n        each service in [{icon:\"laptop-code\",title:\"Web Development\",desc:\"Cutting-edge websites and applications for your business.\"},{icon:\"lock\",title:\"Cybersecurity\",desc:\"Keeping your data and infrastructure secure from threats.\"},{icon:\"cloud\",title:\"Cloud Solutions\",desc:\"Scalable and flexible cloud computing services.\"},{icon:\"chart-line\",title:\"Data Science\",desc:\"Data-driven insights to empower decision-making.\"},{icon:\"cogs\",title:\"DevOps\",desc:\"Streamlined development and operations with automation.\"},{icon:\"robot\",title:\"AI & ML\",desc:\"Smart systems to automate and predict with precision.\"},{icon:\"briefcase\",title:\"IT Consulting\",desc:\"Expert advice and strategy tailored to your goals.\"}]\r\n\r\n          .col-md-4.mb-4.text-center\r\n            i.service-icon.fas(class=`fa-${service.icon}`)\r\n            h4.mt-3= service.title\r\n            p= service.desc\r\n\r\n    // Features/Highlights\r\n    section.section-light.py-5\r\n      .container\r\n        h2.text-center.mb-4 Why Choose Us\r\n        .row.text-center\r\n          each feature in [{icon: \"clock\", title: \"Fast Delivery\"}, {icon: \"user-shield\", title: \"Trusted Experts\"}, {icon: \"thumbs-up\", title: \"Proven Results\"}, {icon: \"handshake\", title: \"Client-Centric\"}]\r\n\r\n            .col-md-3\r\n              i.fas(class=`fa-${feature.icon} service-icon`)\r\n              h5.mt-2= feature.title\r\n\r\n    // Case Studies\r\n    section.container.py-5\r\n      h2.text-center.mb-4 Case Studies\r\n      .row\r\n        .col-md-6\r\n          h5 FinTech Platform Optimization\r\n          p We migrated a legacy financial system to the cloud, reducing costs by 35% and improving uptime to 99.9%.\r\n        .col-md-6\r\n          h5 Healthcare Data Pipeline\r\n          p Built a secure, HIPAA-compliant data pipeline for real-time patient monitoring and analytics.\r\n\r\n    // Testimonials\r\n    section.section-light.py-5\r\n      .container\r\n        h2.text-center.mb-4 What Our Clients Say\r\n        .row\r\n          .col-md-6\r\n            blockquote.blockquote\r\n              p \"Amazing Company transformed our business with their innovative solutions. Highly recommended!\"\r\n              footer - John Doe, CEO of TechCorp\r\n          .col-md-6\r\n            blockquote.blockquote\r\n              p \"Their cybersecurity team helped us secure our infrastructure and prevent major threats.\"\r\n              footer - Jane Smith, Security Lead\r\n\r\n\r\n\r\n    // Call to Action\r\n    section.section-dark.text-center.py-5\r\n      .container\r\n        h2 Ready to Elevate Your Business?\r\n        p Lets build something great together.\r\n        a.btn.btn-outline-light.btn-lg(href=\"#contact\") Contact Us\r\n\r\n    // Contact Section\r\n    section#contact.container.py-5\r\n      h2.text-center.mb-4 Get In Touch\r\n      form\r\n        .mb-3\r\n          label.form-label(for=\"name\") Name\r\n          input.form-control(type=\"text\" id=\"name\" placeholder=\"Your Name\")\r\n        .mb-3\r\n          label.form-label(for=\"email\") Email\r\n          input.form-control(type=\"email\" id=\"email\" placeholder=\"Your Email\")\r\n        .mb-3\r\n          label.form-label(for=\"message\") Message\r\n          textarea.form-control(id=\"message\" rows=\"4\" placeholder=\"Your Message\")\r\n        button.btn.btn-primary Send Message\r\n\r\n    // Footer\r\n    footer.text-center.py-4.bg-dark.text-light\r\n      p &copy; 2025 Amazing Company. All rights reserved.\r\n');
/*!40000 ALTER TABLE `pages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','72b302bf297a228a75730123efef7c41');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-04  1:46:35
