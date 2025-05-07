from manim import *
import numpy as np

class NavierStokesEq(Scene):
    def construct(self):
        title = Title("Navier-Stokes equations")
        self.play(Write(title))
        eq = MathTex(
            r"""
            \frac{\partial u}{\partial t} &= -(u \cdot \nabla) u+\nu \nabla^2 u+\mathbf{f} \\
            \frac{\partial \rho}{\partial t} &= -(u \cdot \nabla) \rho+\kappa \nabla^2 \rho + S
            """,
        ).scale(1).move_to(ORIGIN)
        self.play(Write(eq))
        self.wait(2)

class VelEqBreakdown(Scene):
    def construct(self):
        # Create the full equation
        eq = MathTex(
            r"\frac{\partial u}{\partial t}", 
            r"=", 
            r"-(u \cdot \nabla) u",
            r"+",
            r"\nu \nabla^2 u",
            r"+",
            r"\mathbf{f}"
        ).scale(1.5).move_to(ORIGIN)
        
        # Create explanations for each term
        explanations = [
            "Time derivative of velocity",
            "Advection term",
            "Diffusion term",
            "External forces"
        ]
        
        # Create explanation text
        explanation = Text("", font_size=36).to_edge(DOWN, buff=1)
        
        # Show the full equation
        self.play(Write(eq))
        self.wait(1)
        
        # Define term indices to highlight
        term_indices = [0, 2, 4, 6]  # Indices of the terms in the eq object
        
        # Create an empty highlight box
        highlight_box = None
        
        for i, idx in enumerate(term_indices):
            # Get the part to highlight
            part = eq[idx]
            
            # Create a highlight box around the term
            new_box = SurroundingRectangle(part, buff=0.1, color=YELLOW)
            
            # Animate highlight box and explanation
            if highlight_box is None:
                self.play(
                    Create(new_box),
                    explanation.animate.become(Text(explanations[i], font_size=36).to_edge(DOWN, buff=1))
                )
            else:
                self.play(
                    ReplacementTransform(highlight_box, new_box),
                    explanation.animate.become(Text(explanations[i], font_size=36).to_edge(DOWN, buff=1))
                )
            
            # Update the highlight box reference
            highlight_box = new_box
            
            self.wait(2)
        
        # Remove the final highlight box
        self.play(
            FadeOut(highlight_box),
            explanation.animate.become(Text("", font_size=36).to_edge(DOWN, buff=1))
        )
        
        # Final pause
        self.wait(2)

class DensityEqBreakdown(Scene):
    def construct(self):
        # Create the full equation
        eq = MathTex(
            r"\frac{\partial \rho}{\partial t}", 
            r"=", 
            r"-(u \cdot \nabla) \rho",
            r"+",
            r"\kappa \nabla^2 \rho",
            r"+",
            r"S"
        ).scale(1.5).move_to(ORIGIN)
        
        # Create explanations for each term
        explanations = [
            "Time derivative of density",
            "Advection term",
            "Diffusion term",
            "External sources"
        ]
        
        # Create explanation text
        explanation = Text("", font_size=36).to_edge(DOWN, buff=1)
        
        # Show the full equation
        self.play(Write(eq))
        self.wait(1)
        
        # Define term indices to highlight
        term_indices = [0, 2, 4, 6]  # Indices of the terms in the eq object
        
        # Create an empty highlight box
        highlight_box = None
        
        for i, idx in enumerate(term_indices):
            # Get the part to highlight
            part = eq[idx]
            
            # Create a highlight box around the term
            new_box = SurroundingRectangle(part, buff=0.1, color=YELLOW)
            
            # Animate highlight box and explanation
            if highlight_box is None:
                self.play(
                    Create(new_box),
                    explanation.animate.become(Text(explanations[i], font_size=36).to_edge(DOWN, buff=1))
                )
            else:
                self.play(
                    ReplacementTransform(highlight_box, new_box),
                    explanation.animate.become(Text(explanations[i], font_size=36).to_edge(DOWN, buff=1))
                )
            
            # Update the highlight box reference
            highlight_box = new_box
            
            self.wait(2)
        
        # Remove the final highlight box
        self.play(
            FadeOut(highlight_box),
            explanation.animate.become(Text("", font_size=36).to_edge(DOWN, buff=1))
        )
        
        # Final pause
        self.wait(2)

class GridAnimation(Scene):
    def construct(self):
        # Parameters
        N = 5  # This means we'll have an (N+1)×(N+1) grid (from 0 to N+1)
        cell_size = 0.8
        grid_width = (N + 2) * cell_size
        grid_height = (N + 2) * cell_size
        
        # Create grid
        grid = VGroup()
        
        # Create horizontal and vertical lines
        for i in range(N + 3):  # 0 to N+2 lines
            # Horizontal line
            h_line = Line(
                start=[-grid_width/2, -grid_height/2 + i * cell_size, 0],
                end=[grid_width/2, -grid_height/2 + i * cell_size, 0],
                stroke_width=2,
            )
            grid.add(h_line)
            
            # Vertical line
            v_line = Line(
                start=[-grid_width/2 + i * cell_size, -grid_height/2, 0],
                end=[-grid_width/2 + i * cell_size, grid_height/2, 0],
                stroke_width=2,
            )
            grid.add(v_line)
        
        # Position grid on the left side
        grid.move_to(LEFT * 3)
        
        # Add labels for rows and columns
        labels = VGroup()
        
        # Define symbolic labels
        symbolic_labels = ["0", "1", "2", r"\ldots", "N", "N+1"]
        
        # Column labels (x-axis)
        for i in range(N + 2):  # 0 to N+1
            # Choose the appropriate label
            if i == 0:
                label_text = symbolic_labels[0]  # 0
            elif i == 1:
                label_text = symbolic_labels[1]  # 1
            elif i == 2:
                label_text = symbolic_labels[2]  # 2
            elif i == N:
                label_text = symbolic_labels[4]  # N
            elif i == N + 1:
                label_text = symbolic_labels[5]  # N+1
            else:
                label_text = symbolic_labels[3]  # \ldots
                
            label = MathTex(label_text, font_size=24)
            # Position label at the center of the cell
            label.move_to(
                grid.get_corner(DOWN+LEFT) + 
                [(i + 0.5) * cell_size, -0.5 * cell_size, 0]
            )
            labels.add(label)
        
        # Row labels (y-axis)
        for i in range(N + 2):  # 0 to N+1
            # Choose the appropriate label
            if i == 0:
                label_text = symbolic_labels[0]  # 0
            elif i == 1:
                label_text = symbolic_labels[1]  # 1
            elif i == 2:
                label_text = symbolic_labels[2]  # 2
            elif i == N:
                label_text = symbolic_labels[4]  # N
            elif i == N + 1:
                label_text = symbolic_labels[5]  # N+1
            else:
                label_text = symbolic_labels[3]  # \ldots
                
            label = MathTex(label_text, font_size=24)
            # Position label at the center of the cell
            label.move_to(
                grid.get_corner(DOWN+LEFT) + 
                [-0.5 * cell_size, (i + 0.5) * cell_size, 0]
            )
            labels.add(label)
        
        # Create a text explanation area on the right
        explanation_area = Rectangle(
            width=4,
            height=4,
            stroke_width=0,
            fill_opacity=0
        ).move_to(RIGHT * 3)
        
        # Highlight the boundary cells
        boundary_rects = VGroup()
        
        # Top and bottom rows
        for i in range(N + 2):
            # Bottom row (y=0)
            bottom_rect = Rectangle(
                height=cell_size,
                width=cell_size,
                stroke_opacity=0,
                fill_color=LOGO_BLUE,
                fill_opacity=0.3
            ).move_to(
                grid.get_corner(DOWN+LEFT) + 
                [i * cell_size + cell_size/2, cell_size/2, 0]
            )
            boundary_rects.add(bottom_rect)
            
            # Top row (y=N+1)
            top_rect = Rectangle(
                height=cell_size,
                width=cell_size,
                stroke_opacity=0,
                fill_color=LOGO_BLUE,
                fill_opacity=0.3
            ).move_to(
                grid.get_corner(DOWN+LEFT) + 
                [i * cell_size + cell_size/2, (N+1) * cell_size + cell_size/2, 0]
            )
            boundary_rects.add(top_rect)
        
        # Left and right columns (excluding corners already covered)
        for i in range(1, N + 1):
            # Left column (x=0)
            left_rect = Rectangle(
                height=cell_size,
                width=cell_size,
                stroke_opacity=0,
                fill_color=LOGO_BLUE,
                fill_opacity=0.3
            ).move_to(
                grid.get_corner(DOWN+LEFT) + 
                [cell_size/2, i * cell_size + cell_size/2, 0]
            )
            boundary_rects.add(left_rect)
            
            # Right column (x=N+1)
            right_rect = Rectangle(
                height=cell_size,
                width=cell_size,
                stroke_opacity=0,
                fill_color=LOGO_BLUE,
                fill_opacity=0.3
            ).move_to(
                grid.get_corner(DOWN+LEFT) + 
                [(N+1) * cell_size + cell_size/2, i * cell_size + cell_size/2, 0]
            )
            boundary_rects.add(right_rect)
        
        # Animation
        self.play(Create(grid))
        self.play(Write(labels), run_time=2)
        self.wait(1)
        
        # Show boundary cells
        boundary_label = Text("Boundary Cells", font_size=30).move_to(explanation_area)
        
        self.play(
            FadeIn(boundary_rects),
            Write(boundary_label)
        )
        self.wait(1)
        
        # Show interior cells
        interior_rects = VGroup()
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                interior_rect = Rectangle(
                    height=cell_size,
                    width=cell_size,
                    stroke_opacity=0,
                    fill_color=LOGO_GREEN,
                    fill_opacity=0.3
                ).move_to(
                    grid.get_corner(DOWN+LEFT) + 
                    [i * cell_size + cell_size/2, j * cell_size + cell_size/2, 0]
                )
                interior_rects.add(interior_rect)
        
        interior_label = Text("Interior Cells", font_size=30).move_to(explanation_area)
        
        self.play(FadeOut(boundary_label))
        self.play(
            FadeIn(interior_rects),
            Write(interior_label),
        )
        self.wait(2)

class SimulationStepsAnimation(Scene):
    def construct(self):
        # Parameters
        N = 3  # Smaller grid size for this animation
        cell_size = 0.5
        grid_width = (N + 2) * cell_size
        grid_height = (N + 2) * cell_size
        
        # Function to create a grid
        def create_grid(position, title_text):
            grid_group = VGroup()
            
            # Create the grid lines
            grid = VGroup()
            for i in range(N + 3):  # 0 to N+2 lines
                # Horizontal line
                h_line = Line(
                    start=[-grid_width/2, -grid_height/2 + i * cell_size, 0],
                    end=[grid_width/2, -grid_height/2 + i * cell_size, 0],
                    stroke_width=1.5,
                )
                grid.add(h_line)
                
                # Vertical line
                v_line = Line(
                    start=[-grid_width/2 + i * cell_size, -grid_height/2, 0],
                    end=[-grid_width/2 + i * cell_size, grid_height/2, 0],
                    stroke_width=1.5,
                )
                grid.add(v_line)
            
            # Position grid
            grid.move_to(position)
            grid_group.add(grid)
            
            # Add title
            title = Text(title_text, font_size=24)
            title.next_to(grid, UP, buff=0.3)
            grid_group.add(title)
            
            return grid_group, grid
        
        # Create four grids with titles
        spacing = 3.5  # Horizontal spacing between grids
        
        grid1_group, grid1 = create_grid(LEFT * spacing * 1.5, "Initial Density")
        grid2_group, grid2 = create_grid(LEFT * spacing * 0.5, "Add Forces")
        grid3_group, grid3 = create_grid(RIGHT * spacing * 0.5, "Diffuse")
        grid4_group, grid4 = create_grid(RIGHT * spacing * 1.5, "Move")
        
        # Create arrows between grids
        arrow1 = Arrow(
            start=grid1.get_right() + RIGHT * 0.1,
            end=grid2.get_left() + LEFT * 0.1,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        
        arrow2 = Arrow(
            start=grid2.get_right() + RIGHT * 0.1,
            end=grid3.get_left() + LEFT * 0.1,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        
        arrow3 = Arrow(
            start=grid3.get_right() + RIGHT * 0.1,
            end=grid4.get_left() + LEFT * 0.1,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        
        # Create elbow arrow that loops back from Move to Initial Density
        midpoint_arrow1 = arrow1.get_center()
        
        # Create points for the elbow path
        elbow_start = grid4.get_right() + RIGHT * 0.1
        elbow_point1 = np.array([elbow_start[0] + 0.5, elbow_start[1], 0])  # Right
        elbow_point2 = np.array([elbow_point1[0], midpoint_arrow1[1] - 1.5, 0])  # Down
        elbow_point3 = np.array([midpoint_arrow1[0], elbow_point2[1], 0])  # Left
        elbow_end = np.array([midpoint_arrow1[0], midpoint_arrow1[1] - 0.1, 0])  # Up to arrow1
        
        # Create the elbow path
        elbow_path = VGroup()
        elbow_path.add(Line(elbow_start, elbow_point1))
        elbow_path.add(Line(elbow_point1, elbow_point2))
        elbow_path.add(Line(elbow_point2, elbow_point3))
        elbow_path.add(Line(elbow_point3, elbow_end))
        
        # Add arrowhead to the end of the elbow
        elbow_arrow = Arrow(
            start=elbow_path[-1].get_start(),
            end=elbow_path[-1].get_end(),
            buff=0,
            max_tip_length_to_length_ratio=0.15
        )
        
        # Group the elbow path with the arrowhead
        elbow_loop = VGroup(elbow_path, elbow_arrow)
        
        # Create sample data for visualization in grids
        
        # Initial density - random pattern
        density_rects = VGroup()
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                opacity = np.random.uniform(0.1, 0.5) if np.random.random() > 0.7 else 0
                rect = Rectangle(
                    height=cell_size,
                    width=cell_size,
                    stroke_opacity=0,
                    fill_color=RED,
                    fill_opacity=opacity
                ).move_to(
                    grid1.get_corner(DOWN+LEFT) + 
                    [i * cell_size + cell_size/2, j * cell_size + cell_size/2, 0]
                )
                density_rects.add(rect)
        
        # Add forces - stronger density in center
        forces_rects = VGroup()
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                # Calculate distance from center
                center_i, center_j = (N + 1) / 2, (N + 1) / 2
                dist = np.sqrt((i - center_i)**2 + (j - center_j)**2)
                max_dist = np.sqrt(2) * N / 2
                
                # Higher opacity in center
                opacity = max(0, 0.8 - dist / max_dist)
                if i == center_i and j == center_j:
                    opacity = 0.9  # Peak at center
                
                rect = Rectangle(
                    height=cell_size,
                    width=cell_size,
                    stroke_opacity=0,
                    fill_color=RED,
                    fill_opacity=opacity
                ).move_to(
                    grid2.get_corner(DOWN+LEFT) + 
                    [i * cell_size + cell_size/2, j * cell_size + cell_size/2, 0]
                )
                forces_rects.add(rect)
        
        # Diffuse - smoother transition
        diffuse_rects = VGroup()
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                # Calculate distance from center with smoother falloff
                center_i, center_j = (N + 1) / 2, (N + 1) / 2
                dist = np.sqrt((i - center_i)**2 + (j - center_j)**2)
                max_dist = np.sqrt(2) * N / 2
                
                # Smoother gradient
                opacity = max(0, 0.7 - (dist / max_dist) * 0.7)
                
                rect = Rectangle(
                    height=cell_size,
                    width=cell_size,
                    stroke_opacity=0,
                    fill_color=RED,
                    fill_opacity=opacity
                ).move_to(
                    grid3.get_corner(DOWN+LEFT) + 
                    [i * cell_size + cell_size/2, j * cell_size + cell_size/2, 0]
                )
                diffuse_rects.add(rect)
        
        # Move - shift pattern to simulate advection
        move_rects = VGroup()
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                # Calculate distance from shifted center to simulate movement
                # Shift to upper right
                shift_i, shift_j = 0.5, 0.5
                center_i, center_j = (N + 1) / 2 + shift_i, (N + 1) / 2 + shift_j
                dist = np.sqrt((i - center_i)**2 + (j - center_j)**2)
                max_dist = np.sqrt(2) * N / 2
                
                # Smoother gradient with shift
                opacity = max(0, 0.7 - (dist / max_dist) * 0.7)
                
                rect = Rectangle(
                    height=cell_size,
                    width=cell_size,
                    stroke_opacity=0,
                    fill_color=RED,
                    fill_opacity=opacity
                ).move_to(
                    grid4.get_corner(DOWN+LEFT) + 
                    [i * cell_size + cell_size/2, j * cell_size + cell_size/2, 0]
                )
                move_rects.add(rect)
        
        # Animation sequence
        # Show grids and titles first
        self.play(
            Create(grid1_group),
            Create(grid2_group),
            Create(grid3_group),
            Create(grid4_group),
        )
        self.wait(0.5)
        
        # Show arrows
        self.play(
            Create(arrow1),
            Create(arrow2),
            Create(arrow3),
        )
        self.wait(0.5)
        
        # Show the data in each grid sequentially
        self.play(FadeIn(density_rects))
        self.wait(0.5)
        
        self.play(FadeIn(forces_rects))
        self.wait(0.5)
        
        self.play(FadeIn(diffuse_rects))
        self.wait(0.5)
        
        self.play(FadeIn(move_rects))
        self.wait(1)
        
        # Show the loop back arrow
        self.play(Create(elbow_path), Create(elbow_arrow))
        self.wait(1)
        
        # Add text to explain the loop
        loop_text = Text("Repeat each timestep", font_size=20)
        # Position the text below the horizontal section of the elbow arrow
        text_position = (elbow_point2 + elbow_point3) / 2  # Middle of the bottom horizontal line
        text_position += DOWN * 0.3  # Move down a bit from the line
        loop_text.move_to(text_position)
        self.play(Write(loop_text))
        self.wait(2)

