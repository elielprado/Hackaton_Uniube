USE [SunMonitor]
GO
/****** Object:  Table [dbo].[Client]    Script Date: 10/12/2023 15:15:34 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Client](
	[Client_ID] [int] IDENTITY(1,1) NOT NULL,
	[Company] [int] NOT NULL,
	[Name] [varchar](100) NOT NULL,
	[Address] [varchar](150) NOT NULL,
	[Email] [varchar](100) NOT NULL,
	[Login_User] [varchar](50) NOT NULL,
	[Login_Password] [varchar](50) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Client_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Company]    Script Date: 10/12/2023 15:15:35 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Company](
	[Company_ID] [int] IDENTITY(1,1) NOT NULL,
	[Company_Name] [varchar](100) NOT NULL,
	[Capacity] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[Company_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SolarBoards]    Script Date: 10/12/2023 15:15:35 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SolarBoards](
	[SolarBoards_ID] [int] IDENTITY(1,1) NOT NULL,
	[Status] [varchar](50) NOT NULL,
	[Alarms] [bit] NOT NULL,
	[Company] [int] NOT NULL,
	[Client] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[SolarBoards_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Client]  WITH CHECK ADD FOREIGN KEY([Company])
REFERENCES [dbo].[Company] ([Company_ID])
GO
ALTER TABLE [dbo].[SolarBoards]  WITH CHECK ADD FOREIGN KEY([Client])
REFERENCES [dbo].[Client] ([Client_ID])
GO
ALTER TABLE [dbo].[SolarBoards]  WITH CHECK ADD FOREIGN KEY([Company])
REFERENCES [dbo].[Company] ([Company_ID])
GO
