package simulacion.view;

import simulacion.model.RandomValue;
import javax.imageio.ImageIO;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public final class Grafica {
    private static final int WIDTH = 1100, HEIGHT = 550, MARGIN = 70;

    public void save(List<RandomValue> first, List<RandomValue> second, Path output) throws IOException {
        BufferedImage image = new BufferedImage(WIDTH, HEIGHT, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = image.createGraphics();
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, WIDTH, HEIGHT);
        for (int division = 0; division <= 5; division++) {
            int y = MARGIN + division * (HEIGHT - 2 * MARGIN) / 5;
            g.setColor(new Color(220, 220, 220));
            g.drawLine(MARGIN, y, WIDTH - MARGIN, y);
            g.setColor(Color.BLACK);
            g.drawString(String.format("%.1f", 1.0 - division / 5.0), 30, y + 5);
        }
        g.drawLine(MARGIN, MARGIN, MARGIN, HEIGHT - MARGIN);
        g.drawLine(MARGIN, HEIGHT - MARGIN, WIDTH - MARGIN, HEIGHT - MARGIN);
        drawSeries(g, first, new Color(37, 99, 235));
        drawSeries(g, second, new Color(220, 38, 38));
        g.setColor(Color.BLACK);
        g.drawString("Grafica de dispersion - Java", WIDTH / 2 - 90, 25);
        g.drawString("Numero de observacion n", WIDTH / 2 - 75, HEIGHT - 20);
        g.drawString("U(n)", MARGIN, 50);
        g.setColor(new Color(37, 99, 235));
        g.fillRect(WIDTH - 280, 18, 15, 15);
        g.setColor(Color.BLACK);
        g.drawString("Semilla 12345", WIDTH - 260, 31);
        g.setColor(new Color(220, 38, 38));
        g.fillRect(WIDTH - 155, 18, 15, 15);
        g.setColor(Color.BLACK);
        g.drawString("Semilla 67890", WIDTH - 135, 31);
        g.dispose();
        Files.createDirectories(output.getParent());
        ImageIO.write(image, "png", output.toFile());
        System.out.println("Gráfica conjunta de Java: " + output);
    }

    private void drawSeries(Graphics2D g, List<RandomValue> values, Color color) {
        int plotWidth = WIDTH - 2 * MARGIN, plotHeight = HEIGHT - 2 * MARGIN;
        int denominator = Math.max(1, values.size() - 1);
        g.setColor(color);
        for (int index = 0; index < values.size(); index++) {
            int x = MARGIN + (int) Math.round(index * (double) plotWidth / denominator);
            int y = HEIGHT - MARGIN - (int) Math.round(values.get(index).normalized() * plotHeight);
            g.fillOval(x - 1, y - 1, 3, 3);
        }
    }
}
