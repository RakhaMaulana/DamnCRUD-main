FROM php:8.0-apache

# Atur Workdir
WORKDIR /var/www/html

# Salin semua file ke dalam container
COPY . .

# Hapus folder yang tidak perlu langsung saat build (lebih aman)
RUN rm -rf .git .github

# Install ekstensi PHP yang dibutuhkan (jika perlu)
RUN docker-php-ext-install pdo_mysql

# Set permission (opsional, tergantung kebutuhan)
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

# Expose port 80
EXPOSE 80

# Jalankan Apache saat container dimulai
CMD ["apache2-foreground"]
