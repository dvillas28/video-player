"""
Para controlar el script desde aqui
"""

import pygame
import subprocess
import os
import time

# Initialize pygame
pygame.init()

# Create a display surface (for the still image)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen.width = screen.get_rect().width
# screen.height = screen.get_rect().height

# Load your still image
# image_path = "/path/to/your/still/image.jpg"
# image = pygame.image.load(image_path)

# Create a clock object to control frame rate
clock = pygame.time.Clock()

# Start the Bash script as a subprocess
bash_process = subprocess.Popen(["./video_player.sh"],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                shell=True)
# print(bash_process)


# Function to display the still image
def display_still_image():
    # screen.blit(image, (0, 0))
    screen.fill((0, 0, 0))
    pygame.display.flip()


# Main loop
running = True
display_still_image()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            key_pressed = chr(event.key)
            print(key_pressed)

            # Send the key to the Bash script
            bash_process.stdin.write(key_pressed + "\n")
            bash_process.stdin.flush()

    # Check if the Bash script has finished
    if bash_process.poll() is not None:
        break

    # Redraw the still image
    display_still_image()

    # Control frame rate
    clock.tick(30)

# Close the subprocess
bash_process.stdin.close()
bash_process.stdout.close()
bash_process.stderr.close()
bash_process.terminate()

# Quit pygame
pygame.quit()
